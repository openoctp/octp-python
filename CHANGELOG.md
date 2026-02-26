# Changelog

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] — 2026-02-26

### Added

- **Runner Profiles** — Four optimized profiles for different workflows:
  - `fast`: 3-8 seconds, essential checks only (ruff, bandit, detect-secrets)
  - `ci`: 30-60 seconds, balanced coverage (pytest, ruff, bandit, pip-audit, detect-secrets)
  - `security`: 30-60 seconds, security-focused (bandit, pip-audit, detect-secrets, semgrep)
  - `full`: 2-4 minutes, comprehensive (all 7 runners)
  - Select via `--profile` flag or `default_profile` in config

- **Parallel Execution** — Runners now execute in parallel using ThreadPoolExecutor
  - 40-60% faster execution on multi-core machines
  - Graceful handling of runner crashes

- **New Runners**:
  - `ruff_runner`: Python linting (Rust-based, very fast)
  - `mypy_runner`: Type checking for typed codebases
  - `detect_secrets_runner`: Secret and credential detection

- **Non-Interactive Mode** — Automatic detection of non-TTY environments
  - Uses sensible defaults (AI-assisted, substantial review)
  - Shows warning when falling back to defaults
  - Supports `--yes` flag to suppress warnings
  - Honest AI disclosure with both Claude and Kimi listed

- **Honest AI Disclosure** — Default provenance for OCTP project:
  - Method: `ai_assisted_human_reviewed`
  - AI tools: Claude (Anthropic) and Kimi (Moonshot)
  - Review level: `substantial_modification`
  - Demonstrates the tool's own use case

- **Comprehensive Test Suite** — 20 tests covering:
  - Envelope parsing and validation
  - Integrity/hashing
  - Runner profiles and parallel execution
  - Performance benchmarks

- **Documentation** — Complete documentation suite:
  - `installation.md`: Platform-specific install guides
  - `quickstart.md`: 5-minute getting started
  - `profiles.md`: Detailed profile comparison
  - `configuration.md`: `.octp.toml` reference
  - `ci-integration.md`: GitHub Actions, GitLab CI, etc.
  - `troubleshooting.md`: Common issues and solutions

### Changed

- **Improved Test Display** — Tests now show:
  - ✓ passed — Tests ran and passed
  - ✗ failed — Tests ran and failed
  - ○ skipped — Tests not run (appropriate profile)

- **Better Error Handling** — Graceful degradation:
  - Handles missing verification tools
  - Handles network timeouts (pip-audit, safety)
  - Handles interactive prompt failures
  - Continues with available tools

- **Code Quality** — Full ruff and mypy compliance
  - All code passes linting
  - Type annotations throughout
  - Clean test fixtures

### Fixed

- **Non-Interactive Crashes** — Tool no longer crashes when prompts fail
- **Template Text in READMEs** — Removed placeholder text
- **Runner Base Class** — Fixed abstract method declaration
- **Import Ordering** — Fixed all ruff I001 errors
- **Detect-Secrets Exception** — Changed bare except to specific JSONDecodeError

### Removed

- **Safety Runner** — Removed as duplicate of pip-audit
  - Both check for known CVEs in dependencies
  - pip-audit is faster and more reliable
  - Safety remains in codebase but not in profiles

## [0.1.0] — 2026-02-26

### Added

- Initial release of the OCTP reference implementation
- Core envelope generation with `octp sign`
- Envelope verification with `octp verify`
- Repository initialization with `octp init`
- Pydantic envelope model implementing OCTP spec v0.1
- ES256 cryptographic signing via the cryptography library
- Automatic keypair generation and management
- Git integration via GitPython
- Verification runners:
  - pytest_runner: Test execution
  - semgrep_runner: Static analysis
  - bandit_runner: Security scanning
  - deps_runner: Dependency vulnerability check (pip-audit)
- Rich terminal output with human-readable trust summary
- `.octp.toml` project configuration
- JSON Schema for envelope validation
- Example envelopes (minimal and full)
- RFC process and governance structure
- CONTRIBUTING.md and CODE_OF_CONDUCT.md

[Unreleased]: https://github.com/openoctp/octp-python/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/openoctp/octp-python/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/openoctp/octp-python/releases/tag/v0.1.0