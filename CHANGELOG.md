# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [3.3.0] - 2026-11-10

### Added
- `data/directory-catalog.md`: 1,233 unique directories, launch platforms, marketplaces, and social channels with submission URLs, split into 23 verified no-login, 890 free, and 320 paid entries.
- Catalog validation tests for size, unique URLs, sections, and encoding.

### Changed
- Stage 1 now points to the catalog as a research resource and explicitly forbids mass submission.
- README explains how to filter the catalog with the existing quality gates.

## [3.2.0] - 2026-11-10

### Added
- `close_tabs_after_submission` parameter, enabled by default.
- Tab lifecycle policy: one active tab per donor, close after logging, never close operator tabs.
- Report now confirms that all skill tabs are closed.

### Changed
- Verification and logging stages close their temporary tabs immediately after the result is written.

## [3.1.0] - 2026-11-10

### Added
- Search engine reference for the 12 supported locales: `data/search-engines.md` and `data/search-engines.json`, covering own-index engines, index resellers, and crawl-only engines.
- Persistent identity policy: one disposable inbox stored outside the repository at `~/.config/opencode/link-building/identity.json` and reused for every registration.
- `scripts/inbox.py` to read the persistent inbox, wait for verification messages, and extract OTP codes.
- Search engine submission stage (1b) with IndexNow, webmaster tools, and public form guidance.
- Tests for the engine reference, locale coverage, and inbox helpers.

### Changed
- Registration no longer creates a new inbox per donor; it loads the persistent identity and reuses it.
- Quick start and installation docs now describe the persistent inbox setup.
- Case study updated with two live nofollow listings, five pending submissions, and documented paid and CAPTCHA handoffs.

## [3.0.0] - 2026-11-10

### Added
- English skill definition with keyword-rich metadata for GitHub and skill-discovery search.
- Donor scoring rubric, quality gates, and explicit audit mode.
- Verification stage with HTTP status and link attribute (`dofollow`/`nofollow`) recording.
- Repository metadata: MIT license, changelog, contributing guide, CI workflow.
- JSON schema validator (`tests/validate_results.py`) with unit tests and fixtures.
- `data/donor-sources.md` with query families and vetted source categories.
- Real campaign case study for a password generator.

### Changed
- Results log schema is now validated: required fields, ISO-8601 UTC timestamps, allowed statuses, numeric ranges.
- Campaign summary is produced from verified records only; nothing is reported as live without a check.
- Registration flow stops on CAPTCHA, SMS, and ID verification instead of bypassing them.

## [2.1.0] - 2026-04-25

### Added
- Mandatory JSON logging after every attempt.
- OTP retrieval with operator fallback.
- Screenshot capture per successful publication.

## [2.0.0] - 2026-04-20

### Added
- Temp-mail integration through the `temp-mail-automation` skill.
- Multi-donor campaign flow with attempt budgeting.

## [1.0.0] - 2026-04-15

### Added
- Initial skill: donor search, registration, posting, and a simple results file.
