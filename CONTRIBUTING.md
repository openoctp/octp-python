# Contributing to octp-python

## Before you start

Read the OCTP specification: https://github.com/openoctp/spec  
Check open issues to avoid duplicate work.  
For anything beyond a small bug fix — open an issue first.

## What we want in v0.1

- Bug fixes with reproduction cases and tests
- New verification runners for additional tools and languages
- Documentation improvements
- Test coverage improvements

## What we are NOT accepting yet

- New CLI commands beyond sign/verify/init
- Changes to the envelope schema (those go through the spec RFC process)
- Architectural changes to the signing model
- New dependencies without prior discussion

## Setup

```bash
git clone https://github.com/openoctp/octp-python
cd octp-python
pip install -e ".[dev]"
```

## Running tests

```bash
pytest
```

## Code style

```bash
ruff check src/ tests/
mypy src/
```

Both must pass before submitting a PR.

## Pull request process

- One thing per PR
- Reference the issue it closes: `Closes #123`
- Tests required for new behaviour
- Update CHANGELOG.md under Unreleased
- You will receive a response within 72 hours

## Commit message format

```
type: short description

Longer explanation if needed.

Closes #123
```

Types: `fix`, `feat`, `docs`, `test`, `refactor`, `chore`

## Code of conduct

See CODE_OF_CONDUCT.md.