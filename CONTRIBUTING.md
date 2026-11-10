# Contributing

Thanks for improving the Link Building Skill. This project favors **quality over volume** and keeps every automation auditable.

## Ground rules

- White-hat only. No PBNs, link exchanges, paid-link schemes, comment spam, or fake accounts.
- New automation must record its outcome in the results log.
- Anything that can publish to a third-party site must support an approval pause.
- Keep the skill usable in a single `SKILL.md`; supporting files are optional helpers.

## Development setup

```bash
git clone https://github.com/devcodex2025/link-building-skills.git
cd link-building-skills
python -m unittest discover -s tests -v
```

No third-party dependencies are required: the validator and tests use the Python standard library.

## What to contribute

- **Donor sources** — directories, communities, and catalogs that accept relevant submissions. Add them to `data/donor-sources.md` with a note on cost, account requirement, and link type.
- **Scoring heuristics** — better relevance signals, spam detection, or duplicate handling.
- **Validation** — new schema checks and fixtures.
- **Docs** — clearer examples, translations, and failure-handling notes.

## Pull request checklist

- [ ] `python -m unittest discover -s tests -v` passes.
- [ ] `python tests/validate_results.py examples/link_building_results.json` prints `OK`.
- [ ] `SKILL.md` describes any new behavior and guardrail.
- [ ] `CHANGELOG.md` has an entry under `Unreleased`.
- [ ] No credentials, personal data, or private campaign logs are committed.

## Reporting a bad donor

Open an issue with the domain, the submission URL, and what went wrong (paid-only, nofollow-only, rejected disposable email, spam network). Do not include account credentials.
