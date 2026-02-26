# Configuration Reference

OCTP uses `.octp.toml` for repository-specific configuration.

## Creating Configuration

```bash
# Auto-generate with defaults
octp init

# Or create manually
touch .octp.toml
```

## Complete Configuration File

```toml
# .octp.toml - OCTP Configuration

[policy]
# Require envelope for contributions
require_envelope = true

# Minimum review level required
# Options: none, glance, moderate_review, substantial_modification, complete_rewrite
minimum_review_level = "moderate_review"

# Block merging if tests fail
block_on_failed_tests = true

# Allow AI-generated code without human review
allow_unreviewed_ai = false

[runners]
# Default profile when none specified
# Options: fast, ci, security, full
default_profile = "ci"

# Individual runner configuration
test_runner = "pytest"
linting = "ruff"
type_checking = "mypy"
static_analysis = "semgrep"
security_scan = "bandit"
dependency_check = "pip-audit"
secret_detection = "detect-secrets"

[identity]
# Require signed envelopes
require_signed_envelope = true

# Key registry for verification
# Options: github, gitlab, custom URL
key_registry = "github"

# Optional: Custom key server URL
# key_server = "https://keys.example.com"

# OCTP Project Configuration
# This project is built with AI assistance
[provenance]
expected_method = "ai_assisted_human_reviewed"
ai_tools = [
    { model = "claude-sonnet-4-6", vendor = "anthropic", usage = "architecture_and_implementation" },
    { model = "kimi-k2.5", vendor = "moonshot", usage = "implementation_and_scaffolding" }
]
```

## Section: [policy]

Controls repository acceptance criteria.

### require_envelope

```toml
require_envelope = true  # or false
```

When `true`, the repository expects all contributions to include an OCTP envelope. CI/CD can check for this.

### minimum_review_level

```toml
minimum_review_level = "moderate_review"
```

Minimum human review level required:

- `none` — No review required
- `glance` — Brief look
- `moderate_review` — Read and understood
- `substantial_modification` — Significantly changed (default)
- `complete_rewrite` — Almost entirely rewritten

### block_on_failed_tests

```toml
block_on_failed_tests = true  # or false
```

If `true`, contributions with failing tests should not be merged.

### allow_unreviewed_ai

```toml
allow_unreviewed_ai = false  # or true
```

Whether to accept code marked as `ai_generated_unreviewed`.

**Security recommendation:** Set to `false` for production repositories.

## Section: [runners]

Configure verification runners.

### default_profile

```toml
default_profile = "ci"
```

Default profile when running `octp sign` without `--profile`:

- `fast` — Quick checks (3-8 seconds)
- `ci` — Balanced coverage (30-60 seconds)
- `security` — Security-focused (30-60 seconds)
- `full` — Comprehensive (2-4 minutes)

### Individual Runners

Map tool names to categories:

```toml
[runners]
test_runner = "pytest"      # or "unittest", "nose"
linting = "ruff"            # or "flake8", "pylint"
type_checking = "mypy"      # or "pyright"
static_analysis = "semgrep" # or "pylint"
security_scan = "bandit"    # or "safety"
dependency_check = "pip-audit"  # or "safety"
secret_detection = "detect-secrets"
```

**Note:** Tool must be installed separately:

```bash
pip install pytest ruff mypy semgrep bandit pip-audit detect-secrets
```

## Section: [identity]

Identity verification settings.

### require_signed_envelope

```toml
require_signed_envelope = true
```

Require cryptographic signatures on envelopes. Verifies the contributor's identity.

### key_registry

```toml
key_registry = "github"
```

Where to look up public keys for signature verification:

- `github` — Use github.com/{user}.keys
- `gitlab` — Use GitLab user keys API
- Custom URL — Point to your own key server

## Section: [provenance] (Optional)

**For OCTP projects only.** Declares expected AI usage patterns.

```toml
[provenance]
expected_method = "ai_assisted_human_reviewed"
ai_tools = [
    { model = "claude-sonnet-4-6", vendor = "anthropic", usage = "refactoring" },
    { model = "gpt-4", vendor = "openai", usage = "documentation" }
]
```

This serves as documentation, not enforcement. It tells contributors: "This project is built with AI assistance, and that's okay."

## Configuration Examples

### Example 1: Strict Enterprise Policy

```toml
[policy]
require_envelope = true
minimum_review_level = "substantial_modification"
block_on_failed_tests = true
allow_unreviewed_ai = false

[runners]
default_profile = "full"
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

**Use case:** Production code, high security requirements.

### Example 2: Open Source Library

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
security_scan = "bandit"
dependency_check = "pip-audit"
secret_detection = "detect-secrets"

[identity]
require_signed_envelope = false  # Don't require signatures
```

**Use case:** Community-driven project, lower barrier to entry.

### Example 3: Internal Tooling

```toml
[policy]
require_envelope = false  # Optional
minimum_review_level = "glance"
block_on_failed_tests = false
allow_unreviewed_ai = true

[runners]
default_profile = "fast"
linting = "ruff"
security_scan = "bandit"
```

**Use case:** Internal scripts, prototyping, non-critical code.

### Example 4: Security-Critical

```toml
[policy]
require_envelope = true
minimum_review_level = "complete_rewrite"
block_on_failed_tests = true
allow_unreviewed_ai = false

[runners]
default_profile = "security"
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

**Use case:** Authentication, payments, encryption libraries.

## Environment-Specific Configuration

### CI/CD Override

Some CI systems need different timeouts. Create `.octp-ci.toml`:

```toml
[runners]
# Increase timeouts for slow CI runners
test_runner = "pytest --timeout=300"
```

Then in CI:

```bash
OCTP_CONFIG=.octp-ci.toml octp sign --profile ci --yes
```

### Developer Override

Developers can override with `~/.octprc` (not yet implemented):

```toml
# ~/.octprc - Personal defaults
[defaults]
profile = "fast"
```

## Validation

Check your configuration:

```bash
# OCTP validates config on every run
octp sign --dry-run  # Future feature

# For now, just test it works
octp init
octp sign --profile fast --yes
```

## Migration

### From v0.1 to v0.2

Old format:
```toml
[runners]
test_runner = "pytest"
static_analysis = "semgrep"
dependency_check = "pip-audit"
```

New format (backward compatible):
```toml
[runners]
default_profile = "ci"  # New
test_runner = "pytest"
linting = "ruff"        # New
type_checking = "mypy"  # New
static_analysis = "semgrep"
security_scan = "bandit"      # New
dependency_check = "pip-audit"
secret_detection = "detect-secrets"  # New
```

## Best Practices

1. **Commit .octp.toml to repository** — Share configuration with team
2. **Start with `ci` profile** — Good balance for most projects
3. **Require signatures for production** — Adds cryptographic identity
4. **Document AI policy** — Use [provenance] section
5. **Keep it simple** — Don't over-configure

## See Also

- [Runner Profiles](profiles.md) — Choose the right profile
- [Quick Start](quickstart.md) — Get started fast
- [CI Integration](ci-integration.md) — Automate in pipelines