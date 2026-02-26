# OCTP — Open Contribution Trust Protocol

[![Tests](https://github.com/openoctp/octp-python/workflows/Tests/badge.svg)](https://github.com/openoctp/octp-python/actions)
[![Python Versions](https://img.shields.io/pypi/pyversions/octp-python.svg)](https://pypi.org/project/octp-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

> **Honest infrastructure for AI-assisted open source.**

Generate and verify cryptographically signed trust envelopes for every code contribution. Declare AI assistance, verification status, and human review level in a machine-readable format that maintainers can trust.

## Quick Start

```bash
# Install
pip install octp-python

# In any git repository, before submitting a PR
octp sign

# Or use fast mode for quick iteration (3-8 seconds)
octp sign --profile fast --yes
```

**Example envelope output:**
```json
{
  "octp_version": "0.1",
  "contribution_id": "a3f8c2d1-9b4e-4f7a-8c3d-2e1f9a0b5c6d",
  "repository": "github.com/example/webapp",
  "commit_hash": "7f3a9c2b1e4d8f0a6c5b2e9d3f1a7c4b8e2d5f0a",
  "provenance": {
    "method": "ai_assisted_human_reviewed",
    "ai_tools": [
      {"model": "claude-sonnet-4-6", "vendor": "anthropic", "version": "20260215", "usage_type": "refactoring"}
    ],
    "human_review_level": "substantial_modification",
    "human_review_duration_minutes": 47,
    "developer_id": "github:sarah-dev"
  },
  "verification": {
    "tests_passed": true,
    "test_suite_hash": "9c4f2a1b8e3d7f0c5a2b9e4d1f8c3a7b",
    "static_analysis": "passed",
    "static_analysis_tool": "ruff@0.1.15",
    "dependency_check": "passed",
    "novel_dependencies_introduced": false
  },
  "integrity": {
    "payload_hash": "2b4e8f1a9c3d7b0e5f2a8c4d1b9e3f7a0c5d2b8e...",
    "developer_signature": "MEQCIBx3f...",
    "signature_algorithm": "ES256"
  }
}
```

## Why OCTP?

The "AI Slopageddon" is overwhelming maintainers. When every PR could be AI-generated, maintainers need to know:

- Was this written by AI, a human, or both?
- What checks has it passed?
- How carefully was it reviewed?

OCTP creates a **standard vocabulary for trust** — not detection, but honest declaration. Like SSL/TLS solved web trust, OCTP solves contribution trust.

## Installation

```bash
pip install octp-python
```

Requires Python 3.11+.

## Usage

### Interactive Mode (Recommended)

```bash
octp sign
```

Guides you through:
1. **Provenance**: How was this created? (Human-only, AI-assisted, AI-generated)
2. **AI Tools**: Which models were used?
3. **Review Level**: How much human review? (Glance → Complete rewrite)
4. **Duration**: Time spent reviewing
5. **Confidence**: Self-assessed certainty

### Non-Interactive / CI Mode

```bash
# Use defaults (AI-assisted with substantial review)
octp sign --yes

# Fast profile for quick iteration (3-8 seconds)
octp sign --profile fast --yes

# CI profile for pipelines (balanced coverage)
octp sign --profile ci --yes

# Full profile for comprehensive checks (all runners)
octp sign --profile full --yes
```

### Verify Envelopes

```bash
# Check signature integrity and payload hash
octp verify path/to/envelope.json

# Returns: ✓ Envelope is valid — signature verified
# Or: ✗ Envelope is INVALID — [reason]
```

## Runner Profiles

Choose the right verification level for your workflow:

| Profile | Runners | Time | Use Case |
|---------|---------|------|----------|
| `fast` | ruff, bandit, detect-secrets | 3-8s | Quick iteration, daily development |
| `ci` | pytest, ruff, bandit, pip-audit, detect-secrets | 30-60s | CI/CD pipelines |
| `security` | bandit, pip-audit, detect-secrets, semgrep | 30-60s | Security audits |
| `full` | All 7 runners | 2-4min | Comprehensive checks, releases |

### Fast Profile (Default for Development)

```bash
$ octp sign --profile fast --yes

Running verification checks...
  ✓ ruff@0.1.15 — No issues found
  ✓ bandit@1.9.4 — No high-severity issues
  ✗ detect-secrets — Secrets found: 2

Trust Envelope Summary
──────────────────────────────────────────────────
  Repository         github.com/acme/widget
  Commit             a1b2c3d4e5f6...
  Developer          github:jdoe
  Method             ai_assisted_human_reviewed
  Review level       substantial_modification
  Tests              ○ skipped
  Static analysis    passed
  Dependencies       skipped

✓ Envelope signed and written to .octp-envelope.json
```

### CI Profile (For Automated Pipelines)

```bash
$ octp sign --profile ci --yes

Running verification checks...
  ✓ pytest@8.4.2 — 47 passed in 2.31s
  ✓ ruff@0.1.15 — No issues found
  ✓ bandit@1.9.4 — No high-severity issues
  ✓ pip-audit@2.10.0 — No known vulnerabilities
  ✓ detect-secrets — No secrets detected

✓ All checks passed
```

## Configuration

Create `.octp.toml` in your repository root:

```toml
[policy]
require_envelope = true
minimum_review_level = "moderate_review"
block_on_failed_tests = true
allow_unreviewed_ai = false

[runners]
default_profile = "ci"
test_runner = "pytest"
linting = "ruff"
type_checking = "mypy"
static_analysis = "semgrep"
security_scan = "bandit"
dependency_check = "pip-audit"
secret_detection = "detect-secrets"

[identity]
require_signed_envelope = true
key_registry = "github"
```

## Honest AI Disclosure

**This tool was built with AI assistance.** Every commit to octp-python:

- Uses `method: ai_assisted_human_reviewed`
- Lists both Claude (Anthropic) and Kimi (Moonshot) as AI tools
- Undergoes substantial human review before merging
- Is cryptographically signed with full provenance

We believe AI-assisted development with honest disclosure is the future. OCTP is the infrastructure that makes it trustworthy.

## GitHub Actions Integration

Add to `.github/workflows/octp.yml`:

```yaml
name: OCTP Verification

on: [pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - name: Install OCTP
        run: pip install octp-python
      
      - name: Verify envelope exists
        run: |
          if [ ! -f .octp-envelope.json ]; then
            echo "❌ No OCTP envelope found"
            echo "Run: octp sign --profile ci --yes"
            exit 1
          fi
      
      - name: Verify envelope signature
        run: octp verify .octp-envelope.json
```

## Specification

This is the reference implementation of the **Open Contribution Trust Protocol v0.1**.

- 📖 [Read the full specification](https://github.com/openoctp/spec)
- 🏛️ [Governance & RFCs](https://github.com/openoctp/community)
- 💬 [Discussions](https://github.com/openoctp/community/discussions)

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

**Quick setup:**
```bash
git clone https://github.com/openoctp/octp-python
cd octp-python
pip install -e ".[dev]"
pytest
```

## License

MIT License — see [LICENSE](LICENSE) for details.

---

**Built with ❤️ and 🤖 by the open source community.**

[Website](https://octp.dev) • [Specification](https://github.com/openoctp/spec) • [Issues](https://github.com/openoctp/octp-python/issues) • [PyPI](https://pypi.org/project/octp-python/)