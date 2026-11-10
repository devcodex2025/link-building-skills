---
name: link-building
description: White-hat link building and directory submission for a real website. Finds relevant directories, forums, Q&A sites and niche communities, scores donor relevance, creates accounts with a disposable inbox (via temp-mail-automation), verifies OTP codes, publishes a genuinely useful contribution containing the target link, verifies the live URL, and writes an auditable JSON log. Use when asked for link building, backlinks, directory submission, SEO outreach, link prospecting, backlink audit, "submit my site to directories", "build backlinks", "find directories for my tool" or "register and publish a link". Requires only a target URL and a niche.
license: MIT
version: 3.2.0
compatibility: opencode
allowed-tools: browser, web_search, fetch, read, write, edit
metadata:
  author: devcodex2025
  repository: https://github.com/devcodex2025/link-building-skills
  homepage: https://github.com/devcodex2025/link-building-skills#readme
  keywords: link-building, backlinks, seo, directory-submission, off-page-seo, outreach, temp-mail, otp, automation, opencode-skill, ai-agent
  category: seo
---

# Link Building Skill

End-to-end, white-hat link building for a real website. The skill turns a target URL and a niche into vetted donor prospects, completed submissions, verified live links, and a structured results log.

**Core rule:** a link is only worth building if the destination is relevant, the contribution is useful, and the operator can audit exactly what happened.

---

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `target_url` | Yes | — | Page that should receive the backlink. |
| `niche` | Strongly recommended | inferred from the page | Topic used to find and score donors. |
| `max_attempts` | No | `10` | Attempt budget (8–15 recommended). |
| `desired_anchor` | No | auto | Preferred anchor text; variants are generated automatically. |
| `brand_name` | No | from page | Brand used in bios and listings. |
| `allowed_donor_types` | No | all | `directory`, `forum`, `blog_comment`, `qa`, `profile`. |
| `min_relevance` | No | `6` | Relevance threshold, 0–10. |
| `require_approval` | No | `false` | Pause before every publication. |
| `audit_only` | No | `false` | Prospect and score only; never submit. |
| `identity_file` | No | `~/.config/opencode/link-building/identity.json` | Persistent disposable inbox used for every registration. |
| `close_tabs_after_submission` | No | `true` | Close every browser tab opened by the skill once its result is logged. |

If `niche` is missing, derive it from the target page's title, H1, and meta description, and state the inferred niche before proceeding.

### Identity policy

- Use **one** persistent disposable inbox for every registration: directories, search engines, forums, and profiles.
- Read it from `identity_file`. The file contains `provider`, `email`, `password`, `api_base`, and `created_at`.
- Never create a new inbox per donor or per submission.
- Keep the file outside the repository and restrict it to the local user account.
- Rotate the address only if a site rejects it or access is lost, and only with operator approval.
- If a donor requires a branded address, use the operator's branded address instead of the disposable inbox.
- If `temp-mail-automation` is unavailable, use `python scripts/inbox.py list` and `python scripts/inbox.py wait --subject "<text>" --otp` to read the persistent inbox.

### Tab lifecycle

- Close every tab the skill opens as soon as its result is written to the log. Browser tabs are the largest avoidable memory cost in a long campaign.
- Keep at most one active tab per donor during registration and publishing.
- Verification tabs are temporary: close them after reading the result.
- Never close tabs the operator opened manually.
- On a CAPTCHA handoff, leave the tab open until the operator resolves it, then log the outcome and close it.
- If `close_tabs_after_submission` is `false`, keep the tab open only when the operator explicitly asked for it.

---

## Stage 0 — Preflight

1. Load the `temp-mail-automation` skill if it is available and mark whether it is available.
2. Load the persistent identity from `identity_file`. If it does not exist, create exactly one inbox and save it there.
3. Verify the browser session: open a tab and confirm `browser_status` / navigation works.
4. Load `link_building_results.json` from the working directory. If absent, create it with `[]`.
5. Fetch the target URL and record: title, H1, meta description, niche, brand, canonical URL.
6. Confirm the campaign parameters with the operator if any of these are unclear: target URL, niche, budget, approval mode.

Never overwrite an existing log. Only append.

---

## Stage 1 — Donor discovery

Search with multiple query families and record every candidate before vetting:

- `<niche> directory submit tool`
- `<niche> "submit your website" free`
- `best <niche> tools` / `alternatives to <competitor>`
- `site:reddit.com <niche> recommendations` and other niche communities
- `"add your tool" <niche>` / `"suggest a resource" <niche>`
- Startup and tool catalogs relevant to the niche
- Q&A threads that explicitly welcome a relevant resource

Collect for each candidate: URL, donor type, submission URL, account requirement, email policy, link attribute (`dofollow`/`nofollow`/unknown), cost, and moderation notes.

Use [`data/donor-sources.md`](data/donor-sources.md) for source categories, query templates, and a worked set of password-security directories.

---

## Stage 1b — Search engine submission (optional track)

Search engines are not link donors. Do not register accounts on every engine; submit only where an own-index channel exists.

1. Load [`data/search-engines.md`](data/search-engines.md) and [`data/search-engines.json`](data/search-engines.json).
2. Confirm `robots.txt`, `sitemap.xml`, canonical tags, and `hreflang` for every locale.
3. Submit the sitemap once through IndexNow after deploying the key file to the site root.
4. Submit the sitemap to Google, Bing, Yandex, and the Chinese engines where the operator has verified accounts.
5. Use public forms only where no account is needed: Coc Coc, Wiby, Marginalia, LetSearch.
6. Never resubmit a URL that is already pending; record engine, URL, date, and status.
7. Index resellers and crawl-only engines need no submission; optimize for their upstream index instead.

Search engine submissions are not backlinks. Track them separately from `link_building_results.json`.

---

## Stage 2 — Vetting and scoring

Score each candidate 0–10:

| Dimension | Points |
|---|---|
| Topic match | 0–4 |
| Audience overlap | 0–3 |
| Link quality (indexable, in-content or listing body) | 0–2 |
| Submission friction (lower friction, higher score) | 0–1 |

Gates — reject with `status: "skipped"` if any fails:

- relevance < `min_relevance`
- page is `noindex`, login-gated, or does not permit outbound links
- paid-only placement without operator approval
- domain already present in the results log
- site is a link farm, PBN, or auto-generated content network
- site's terms prohibit disposable email and no branded email is available

Maintain a shortlist in the log as `status: "candidate"` records during audit mode. In live mode, candidates move to `pending` or `success` only after a real submission.

---

## Stage 3 — Account creation

For each approved donor:

1. Load the persistent identity from `identity_file`. Do not create a new inbox per donor.
2. Navigate to the registration page and fill the form: email, password, username, and required profile fields.
3. Use a consistent, honest brand identity. Do not impersonate a real person or company.
4. Submit the form.
5. Read the OTP from the persistent inbox and enter it.
   - If no code arrives within 3 minutes, request one resend, wait once more, then ask the operator for the code.
   - If the site rejects disposable domains, stop and log `status: "failed"` with a note.
6. Complete email verification and confirm the account is active.
7. Log in with the same credentials and verify the session.

One account per donor domain. The same persistent address may be reused across donor domains. Never create sockpuppets or vote rings.

---

## Stage 4 — Publishing

1. Read the destination: thread topic, existing replies, moderation tone, formatting rules.
2. Write a contribution of 3–8 sentences that stands on its own without the link. For directory listings, write a factual product description instead.
3. Insert `target_url` once, with a natural anchor:
   - use the desired anchor when supplied;
   - otherwise vary between branded, partial-match, and descriptive anchors;
   - never use the same exact-match anchor more than twice in a campaign.
4. No duplicate copy across donors. Every submission is rewritten for its context.
5. Publish or submit for review.
6. Capture a screenshot of the published state.
7. If a CAPTCHA, phone verification, ID check, or payment appears: pause, keep the browser on the page, and hand control to the operator. Do not attempt to bypass it.
8. After the result is logged, close the tab when `close_tabs_after_submission` is `true` (default). Do not close tabs the operator opened manually.

---

## Stage 5 — Verification

For every submission:

- Open `posted_url` in a fresh request or tab.
- Confirm HTTP 2xx and that the target link is present in the page content.
- Record the link attribute (`rel="nofollow"`, `ugc`, `sponsored`, or `dofollow`).
- If the content is awaiting moderation, record `status: "pending"` and the expected review window.
- If the link is missing or the page 404s, record `status: "failed"` with the observed HTTP status.
- Close the verification tab after the record is written; do not leave it open for the rest of the campaign.

---

## Stage 6 — Logging (mandatory)

Append one record per attempt to `link_building_results.json` immediately after verification. Never batch writes at the end of the run.

After the append succeeds, close the submission tab (`browser.tabs.close`) when `close_tabs_after_submission` is enabled. The record and screenshot are the source of truth; the tab is disposable.

```json
[
  {
    "timestamp": "2026-11-10T09:42:17Z",
    "site_url": "https://toolsdirectoryonline.com",
    "donor_type": "directory",
    "relevance_score": 8,
    "temp_email": "x7k9p2q4@mail.tm",
    "password": "Pass123!Temp",
    "action": "registration_and_listing",
    "anchor_text": "free password generator",
    "target_url": "https://example.com/password-generator",
    "posted_url": "https://toolsdirectoryonline.com/tools/password-generator",
    "status": "success",
    "http_status": 200,
    "link_rel": "dofollow",
    "screenshot": "screenshots/20261110_toolsdirectoryonline.png",
    "otp_used": "748291",
    "notes": "Free listing approved on first review; description matched directory tone."
  }
]
```

Required fields: `timestamp`, `site_url`, `donor_type`, `action`, `target_url`, `status`.
Allowed `status` values: `success`, `pending`, `rejected`, `failed`, `skipped`, `candidate`.
Timestamps are ISO-8601 UTC. URLs must be absolute.

Validate before finishing:

```bash
python tests/validate_results.py link_building_results.json
```

---

## Stage 7 — Report

Summarize for the operator:

- attempts made vs. budget
- successes, pending, rejected, skipped, failed
- dofollow vs. nofollow breakdown
- per-donor one-line reason for skips and failures
- next actions (re-verify pending links, retry transient failures, add new donor sources)
- confirmation that all tabs opened by the skill are closed

Keep the summary factual. Do not claim a link is live unless Stage 5 verified it.

---

## Guardrails

- **Relevance over volume.** Ten relevant listings beat a hundred low-quality ones.
- **One link per contribution.** No link stuffing, no hidden links, no cloaking.
- **Honest identity.** Real brand, real product claims, no fake reviews.
- **Consent for side effects.** Ask before paying, publishing where approval is required, or submitting personal data.
- **Respect limits.** Honor `robots.txt`, rate limits, and each site's submission policy.
- **Stop on anti-bot checks.** CAPTCHA, SMS, and ID verification are operator handoffs, not obstacles to defeat.
- **Close tabs after work.** Every tab opened by the skill is closed after its result is logged; tabs left open waste memory and hide state.
- **No prohibited tactics.** No PBNs, link exchanges, paid links without disclosure, comment spam, or automated account farms.

---

## Failure handling

| Failure | Response |
|---|---|
| Registration form rejects the email domain | Log `failed`; note the restriction; move on. |
| OTP not received | Resend once, wait 3 minutes, then ask the operator. |
| CAPTCHA or phone verification | Pause and hand off to the operator with the browser left on the page. |
| Submission requires payment | Log `skipped` unless the operator approved the cost. |
| Post removed after publication | Update the record to `rejected` with the moderation reason. |
| Session expires mid-run | Re-authenticate with the stored credentials; never create a second account. |

---

## Language triggers

The skill is language-agnostic. It should activate for requests such as:

- "build backlinks for ...", "submit my site to directories", "link building campaign", "off-page SEO"
- "link prospecting", "backlink audit", "find directories for my tool"
- any request that asks to register, publish, and log a link for a target URL

If the request is ambiguous, confirm the target URL and niche before doing any work.
