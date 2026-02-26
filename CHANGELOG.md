# Changelog

## [Unreleased]

## [0.1.0] — 2026-02-26

Initial release of the OCTP reference implementation.

### Added
- `octp sign` — generates and signs a trust envelope for current commit
- `octp verify` — verifies an existing trust envelope
- `octp init` — initialises OCTP configuration in a repository
- Pydantic envelope model implementing OCTP spec v0.1
- ES256 cryptographic signing via the cryptography library
- Automatic keypair generation and management
- Git integration via GitPython
- Verification runners: pytest, semgrep, bandit, pip-audit
- Rich terminal output with human-readable trust summary
- .octp.toml project configuration