#!/usr/bin/env python3
"""Validate a link-building results log.

Usage:
    python tests/validate_results.py path/to/link_building_results.json
    python tests/validate_results.py --strict path/to/log.json

Exit codes:
    0  log is valid
    1  log is structurally valid but has warnings (only with --strict)
    2  log is invalid
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

REQUIRED_FIELDS = (
    "timestamp",
    "site_url",
    "donor_type",
    "action",
    "target_url",
    "status",
)

ALLOWED_STATUS = {"success", "pending", "rejected", "failed", "skipped", "candidate"}
ALLOWED_DONOR_TYPES = {
    "directory",
    "forum",
    "blog_comment",
    "qa",
    "profile",
    "catalog",
    "social",
    "unknown",
}
ALLOWED_LINK_REL = {"dofollow", "nofollow", "ugc", "sponsored", "unknown"}
ISO_8601_Z = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")


def _is_absolute_http_url(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _normalize_domain(value: str) -> str:
    host = (urlparse(value).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def validate(records: object) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for a parsed JSON document."""
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(records, list):
        return ["root element must be a JSON array"], warnings

    seen_domains: dict[str, int] = {}

    for index, record in enumerate(records):
        prefix = f"record[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix}: must be a JSON object")
            continue

        for field in REQUIRED_FIELDS:
            value = record.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(f"{prefix}: missing required field '{field}'")

        status = record.get("status")
        if status is not None and status not in ALLOWED_STATUS:
            errors.append(
                f"{prefix}: invalid status '{status}' "
                f"(allowed: {', '.join(sorted(ALLOWED_STATUS))})"
            )

        donor_type = record.get("donor_type")
        if donor_type is not None and donor_type not in ALLOWED_DONOR_TYPES:
            errors.append(
                f"{prefix}: invalid donor_type '{donor_type}' "
                f"(allowed: {', '.join(sorted(ALLOWED_DONOR_TYPES))})"
            )

        timestamp = record.get("timestamp")
        if isinstance(timestamp, str) and not ISO_8601_Z.match(timestamp):
            errors.append(f"{prefix}: timestamp '{timestamp}' is not ISO-8601 UTC (e.g. 2026-11-10T09:42:17Z)")
        elif isinstance(timestamp, str):
            try:
                datetime.strptime(timestamp.replace("Z", "+0000"), "%Y-%m-%dT%H:%M:%S%z")
            except ValueError:
                errors.append(f"{prefix}: timestamp '{timestamp}' is not a real date")

        for field in ("target_url", "site_url"):
            value = record.get(field)
            if value is not None and not _is_absolute_http_url(value):
                errors.append(f"{prefix}: {field} must be an absolute http(s) URL")

        posted = record.get("posted_url")
        if posted:
            if not _is_absolute_http_url(posted):
                errors.append(f"{prefix}: posted_url must be an absolute http(s) URL")
        elif status == "success":
            errors.append(f"{prefix}: successful record must include posted_url")

        relevance = record.get("relevance_score")
        if relevance is not None:
            if not isinstance(relevance, int) or isinstance(relevance, bool):
                errors.append(f"{prefix}: relevance_score must be an integer 0-10")
            elif not 0 <= relevance <= 10:
                errors.append(f"{prefix}: relevance_score must be between 0 and 10")

        link_rel = record.get("link_rel")
        if link_rel is not None and link_rel not in ALLOWED_LINK_REL:
            errors.append(
                f"{prefix}: invalid link_rel '{link_rel}' "
                f"(allowed: {', '.join(sorted(ALLOWED_LINK_REL))})"
            )

        http_status = record.get("http_status")
        if http_status is not None:
            if not isinstance(http_status, int) or isinstance(http_status, bool):
                errors.append(f"{prefix}: http_status must be an integer")
            elif not 100 <= http_status <= 599:
                errors.append(f"{prefix}: http_status must be a valid HTTP status code")

        site_url = record.get("site_url")
        if isinstance(site_url, str) and site_url:
            domain = _normalize_domain(site_url)
            if domain:
                if domain in seen_domains:
                    warnings.append(
                        f"{prefix}: duplicate domain '{domain}' "
                        f"(first seen in record[{seen_domains[domain]}])"
                    )
                else:
                    seen_domains[domain] = index

        if status == "success" and not record.get("screenshot"):
            warnings.append(f"{prefix}: successful record has no screenshot")

        if status in {"failed", "rejected", "skipped"} and not record.get("notes"):
            warnings.append(f"{prefix}: '{status}' record should explain why in notes")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a link-building results log.")
    parser.add_argument("path", type=Path, help="Path to link_building_results.json")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures.",
    )
    args = parser.parse_args(argv)

    if not args.path.exists():
        print(f"FAIL: file not found: {args.path}")
        return 2

    try:
        data = json.loads(args.path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"FAIL: invalid JSON in {args.path}: {exc}")
        return 2

    errors, warnings = validate(data)

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"FAIL: {error}")

    if errors:
        print(f"FAIL: {len(errors)} error(s) in {len(data) if isinstance(data, list) else '?'} record(s)")
        return 2

    if warnings and args.strict:
        print(f"FAIL (strict): {len(warnings)} warning(s)")
        return 1

    print(f"OK: {len(data)} records valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
