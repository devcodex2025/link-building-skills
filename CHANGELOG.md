# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed
- Expanded the `generatepasswordto.me` pilot: two listings are now live (MeWebLink, Zearches), five submissions await review, and paid-only/captcha handoffs are documented per donor.

## [3.0.0] - 2026-11-10

### Added
- English skill definition with keyword-rich metadata for GitHub and skill-discovery search.
- Donor scoring rubric, quality gates, and explicit audit mode.
- Verification stage with HTTP status and link attribute (`dofollow`/`nofollow`) recording.
- Repository metadata: MIT license, changelog, contributing guide, CI workflow.
- JSON schema validator (`tests/validate_results.py`) with unit tests and fixtures.
- `data/donor-sources.md` with query families and vetted source categories.
- Real campaign case study for `generatepasswordto.me`.

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
