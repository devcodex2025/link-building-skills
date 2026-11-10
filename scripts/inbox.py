#!/usr/bin/env python3
"""Read the persistent disposable inbox used by the link-building skill.

The inbox credentials live outside the repository, by default at:

    ~/.config/opencode/link-building/identity.json

The file is produced by the skill and contains:

    {
      "provider": "mail.tm",
      "email": "...",
      "password": "...",
      "api_base": "https://api.mail.tm"
    }

Usage:
    python scripts/inbox.py list
    python scripts/inbox.py latest
    python scripts/inbox.py wait --from example.com --timeout 180
    python scripts/inbox.py wait --subject "verify" --otp
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_IDENTITY = Path.home() / ".config" / "opencode" / "link-building" / "identity.json"
OTP_PATTERN = re.compile(r"(?<!\d)(\d{4,8})(?!\d)")


def identity_path() -> Path:
    override = os.environ.get("LINK_BUILDING_IDENTITY")
    return Path(override) if override else DEFAULT_IDENTITY


def load_identity(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Identity file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    for field in ("email", "password", "api_base"):
        if not data.get(field):
            raise SystemExit(f"Identity file is missing '{field}': {path}")
    if data.get("provider", "mail.tm") != "mail.tm":
        raise SystemExit(f"Unsupported provider: {data.get('provider')}")
    return data


def request(identity: dict, path: str, method: str = "GET", token: str | None = None, body: dict | None = None) -> dict:
    url = identity["api_base"].rstrip("/") + path
    payload = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {"Accept": "application/json"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code} from {url}: {detail[:300]}")


def login(identity: dict) -> str:
    data = request(
        identity,
        "/token",
        method="POST",
        body={"address": identity["email"], "password": identity["password"]},
    )
    token = data.get("token")
    if not token:
        raise SystemExit("Login succeeded but no token was returned.")
    return token


def list_messages(identity: dict, token: str, limit: int = 20) -> list[dict]:
    data = request(identity, "/messages?page=1", token=token)
    if isinstance(data, list):
        return data[:limit]
    return (data.get("hydra:member") or [])[:limit]


def read_message(identity: dict, token: str, message_id: str) -> dict:
    return request(identity, f"/messages/{message_id}", token=token)


def format_message(message: dict, text: str = "") -> str:
    sender = (message.get("from") or {}).get("address", "unknown")
    lines = [
        f"id:      {message.get('id')}",
        f"from:    {sender}",
        f"subject: {message.get('subject')}",
        f"date:    {message.get('createdAt')}",
    ]
    if text:
        lines.append("")
        lines.append(text.strip())
    return "\n".join(lines)


def matches(message: dict, sender: str | None, subject: str | None) -> bool:
    from_address = ((message.get("from") or {}).get("address") or "").lower()
    message_subject = (message.get("subject") or "").lower()
    if sender and sender.lower() not in from_address:
        return False
    if subject and subject.lower() not in message_subject:
        return False
    return True


def command_list(identity: dict) -> int:
    token = login(identity)
    messages = list_messages(identity, token)
    if not messages:
        print("Inbox is empty.")
        return 0
    for message in messages:
        sender = (message.get("from") or {}).get("address", "unknown")
        print(f"{message.get('createdAt')}  {sender:40}  {message.get('subject')}")
    return 0


def command_latest(identity: dict, otp: bool) -> int:
    token = login(identity)
    messages = list_messages(identity, token, limit=1)
    if not messages:
        print("Inbox is empty.")
        return 0
    full = read_message(identity, token, messages[0]["id"])
    text = full.get("text") or ""
    print(format_message(full, text))
    if otp:
        codes = OTP_PATTERN.findall(text)
        print("\nOTP candidates:", ", ".join(codes) if codes else "none found")
    return 0


def command_wait(identity: dict, sender: str | None, subject: str | None, timeout: int, interval: int, otp: bool) -> int:
    token = login(identity)
    deadline = time.time() + timeout
    seen: set[str] = set()
    while time.time() < deadline:
        messages = list_messages(identity, token, limit=50)
        for message in messages:
            if message["id"] in seen:
                continue
            seen.add(message["id"])
            if matches(message, sender, subject):
                full = read_message(identity, token, message["id"])
                text = full.get("text") or ""
                print(format_message(full, text))
                if otp:
                    codes = OTP_PATTERN.findall(text)
                    print("\nOTP candidates:", ", ".join(codes) if codes else "none found")
                return 0
        time.sleep(interval)
    print(f"No matching message within {timeout} seconds.", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read the persistent link-building inbox.")
    parser.add_argument("--identity", type=Path, help="Override the identity file path.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List recent messages.")

    latest = sub.add_parser("latest", help="Show the latest message.")
    latest.add_argument("--otp", action="store_true", help="Extract numeric OTP candidates.")

    wait = sub.add_parser("wait", help="Wait for a matching message.")
    wait.add_argument("--from", dest="sender", help="Substring of the sender address.")
    wait.add_argument("--subject", help="Substring of the subject.")
    wait.add_argument("--timeout", type=int, default=180, help="Seconds to wait (default: 180).")
    wait.add_argument("--interval", type=int, default=5, help="Polling interval in seconds (default: 5).")
    wait.add_argument("--otp", action="store_true", help="Extract numeric OTP candidates.")

    args = parser.parse_args(argv)

    identity_file = args.identity or identity_path()
    identity = load_identity(identity_file)

    if args.command == "list":
        return command_list(identity)
    if args.command == "latest":
        return command_latest(identity, args.otp)
    if args.command == "wait":
        return command_wait(identity, args.sender, args.subject, args.timeout, args.interval, args.otp)
    return 1


if __name__ == "__main__":
    sys.exit(main())
