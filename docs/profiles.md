# Runner Profiles

OCTP provides four built-in profiles optimized for different workflows and time constraints.

## Profile Overview

| Profile | Runners | Typical Time | Best For |
|---------|---------|--------------|----------|
| `fast` | 3 runners | 3-8 seconds | Daily development, quick iteration |
| `ci` | 5 runners | 30-60 seconds | CI/CD pipelines, pre-commit |
| `security` | 4 runners | 30-60 seconds | Security audits, sensitive code |
| `full` | 7 runners | 2-4 minutes | Comprehensive checks, releases |

## Fast Profile

**Purpose:** Quick iteration during development

**Command:**
```bash
octp sign --profile fast --yes
```

**Runners:**
- **ruff**: Python linting (very fast, Rust-based)
- **bandit**: Security scanning (Python-specific)
- **detect-secrets**: Secret detection (no network calls)

**Example Output:**
```
Running verification checks...
  ✓ ruff@0.1.15 — No issues found
  ✓ bandit@1.9.4 — No high-severity issues
  ✗ detect-secrets — Secrets found: 2

Trust Envelope Summary
  Repository         github.com/acme/webapp
  Commit             a1b2c3d4e5f6...
  Method             ai_assisted_human_reviewed
  Tests              ○ skipped
  Static analysis    ✓ passed
  Dependencies       ○ skipped
```

**Notes:**
- Skips tests, type checking, and network-dependent tools
- Fast enough to run before every commit
- Catches linting errors and obvious security issues

**When to use:**
- Writing code iteratively
- Before every commit during feature development
- On slow machines or poor network connections

## CI Profile

**Purpose:** Balanced coverage for automated pipelines

**Command:**
```bash
octp sign --profile ci --yes
```

**Runners:**
- **pytest**: Test suite execution
- **ruff**: Python linting
- **bandit**: Security scanning
- **pip-audit**: Dependency vulnerability check
- **detect-secrets**: Secret detection

**Example Output:**
```
Running verification checks...
  ✓ pytest@8.4.2 — 47 passed in 2.31s
  ✓ ruff@0.1.15 — No issues found
  ✓ bandit@1.9.4 — No high-severity issues
  ✓ pip-audit@2.10.0 — No known vulnerabilities
  ✓ detect-secrets — No secrets detected

✓ All checks passed
```

**Notes:**
- Includes test execution
- Checks for known vulnerabilities in dependencies
- Omits slower tools (mypy, semgrep)

**When to use:**
- Pre-commit hooks
- CI/CD pipelines
- Before submitting pull requests
- When you want solid coverage without extreme wait times

## Security Profile

**Purpose:** Security-focused auditing

**Command:**
```bash
octp sign --profile security --yes
```

**Runners:**
- **bandit**: Python security scanning
- **pip-audit**: Known CVE checking
- **detect-secrets**: Secret/credential detection
- **semgrep**: Advanced pattern matching for security

**Example Output:**
```
Running verification checks...
  ✓ bandit@1.9.4 — No high-severity issues
  ✓ pip-audit@2.10.0 — No known vulnerabilities
  ✓ detect-secrets — No secrets detected
  ✓ semgrep@1.153.0 — No security issues found

Security audit complete
```

**Notes:**
- Skips tests and general linting
- Focuses entirely on security concerns
- Semgrep provides advanced security pattern detection

**When to use:**
- Security audits
- Before handling sensitive data (auth, payments, PII)
- When adding new dependencies
- Compliance requirements

## Full Profile

**Purpose:** Maximum verification coverage

**Command:**
```bash
octp sign --profile full --yes
```

**Runners:**
- **pytest**: Test execution
- **ruff**: Linting
- **mypy**: Type checking
- **semgrep**: Static analysis
- **bandit**: Security scanning
- **pip-audit**: Dependency auditing
- **detect-secrets**: Secret detection

**Example Output:**
```
Running verification checks...
  ✓ pytest@8.4.2 — 47 passed in 2.31s
  ✓ ruff@0.1.15 — No issues found
  ✓ mypy@1.19.1 — Success: no issues found
  ✓ semgrep@1.153.0 — No issues found
  ✓ bandit@1.9.4 — No high-severity issues
  ✓ pip-audit@2.10.0 — No known vulnerabilities
  ✓ detect-secrets — No secrets detected

✓ All checks passed
```

**Notes:**
- Comprehensive but slow
- Type checking (mypy) can be time-consuming
- Semgrep may have longer startup time
- Parallel execution reduces total time

**When to use:**
- Before major releases
- Final PR review
- Compliance audits
- When time is not a constraint

## Comparing Profiles

### Timing Comparison

```bash
# Time each profile
time octp sign --profile fast --yes    # ~5s
time octp sign --profile ci --yes      # ~45s
time octp sign --profile security --yes # ~40s
time octp sign --profile full --yes    # ~150s
```

### What Each Catches

| Issue Type | fast | ci | security | full |
|------------|------|-----|----------|------|
| Linting errors | ✓ | ✓ | — | ✓ |
| Security vulnerabilities | ✓ | ✓ | ✓ | ✓ |
| Secrets in code | ✓ | ✓ | ✓ | ✓ |
| Test failures | — | ✓ | — | ✓ |
| Type errors | — | — | — | ✓ |
| Known CVEs | — | ✓ | ✓ | ✓ |
| Advanced patterns | — | — | ✓ | ✓ |

## Setting a Default Profile

In your `.octp.toml`:

```toml
[runners]
default_profile = "ci"
```

Then simply run:
```bash
octp sign --yes  # Uses ci profile by default
```

## Profile-Specific Examples

### Example 1: Daily Development Loop

```bash
# While coding - use fast
octp sign --profile fast --yes
git add .
git commit -m "WIP: feature X"

# Before push - use ci
octp sign --profile ci --yes
git add .octp-envelope.json
git commit --amend --no-edit
git push
```

### Example 2: Security-Critical Code

```bash
# Before any security-sensitive change
octp sign --profile security --yes

# Review the envelope
cat .octp-envelope.json | jq '.verification'

# Only proceed if all security checks pass
```

### Example 3: Release Preparation

```bash
# Final comprehensive check
octp sign --profile full --yes

# Verify signature
octp verify .octp-envelope.json

# Create release commit
git add .octp-envelope.json
git commit -m "chore: release v1.2.3 with OCTP envelope"
git tag v1.2.3
git push --tags
```

## Custom Profiles (Advanced)

You can create custom runner combinations by specifying individual runners:

```python
# In your automation
from octp.verification.registry import run_all

# Run only specific runners
results = run_all(
    repo_root=Path("."),
    runner_names=["ruff", "pytest"]
)
```

Or via CLI (future feature):
```bash
octp sign --runners ruff,pytest --yes
```

## Troubleshooting by Profile

### Fast Profile Issues

**"No runners available"**
```bash
pip install ruff bandit detect-secrets
```

### CI Profile Timeouts

**pip-audit times out**
```bash
# Check network connectivity
pip-audit --progress-spinner=off

# Use fast profile instead
octp sign --profile fast --yes
```

### Full Profile Slowdown

**mypy takes forever**
- First run is slow (caching)
- Subsequent runs are faster
- Consider using ci profile for daily work

**semgrep times out**
```bash
# Semgrep rules are large, initial download takes time
# It's cached for 24 hours
```

## Recommendations by Workflow

| Workflow | Recommended Profile | Notes |
|----------|---------------------|-------|
| Feature development | `fast` | Run frequently, low overhead |
| Bug fixes | `ci` | Include tests that verify fix |
| Refactoring | `ci` or `full` | Type checking helps catch errors |
| Dependency updates | `security` | Check for new CVEs |
| Documentation | `fast` | Minimal checks needed |
| Release preparation | `full` | Comprehensive validation |
| Security audit | `security` | Focused on security only |
| CI/CD pipeline | `ci` | Balanced coverage and speed |

## See Also

- [Configuration Guide](configuration.md) — Customize `.octp.toml`
- [Quick Start](quickstart.md) — Get started in 5 minutes
- [Troubleshooting](troubleshooting.md) — Common issues and fixes