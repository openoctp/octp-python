# Quick Start Guide

Get your first OCTP envelope generated in under 5 minutes.

## Step 1: Install

```bash
pip install octp-python
```

## Step 2: Navigate to Your Project

```bash
cd /path/to/your/git-repo
```

OCTP only works inside git repositories. It reads repository metadata to bind the envelope to a specific commit.

## Step 3: Initialize OCTP

```bash
octp init
```

This creates a `.octp.toml` configuration file:

```toml
[policy]
require_envelope = true
minimum_review_level = "moderate_review"

[runners]
default_profile = "ci"
test_runner = "pytest"
linting = "ruff"
```

## Step 4: Generate Your First Envelope

### Option A: Interactive (Recommended for Learning)

```bash
octp sign
```

You'll be guided through:

1. **How was this contribution created?**
   ```
   [1] Human only
   [2] AI assisted, human reviewed
   [3] AI generated, human reviewed
   [4] AI generated, unreviewed
   ```

2. **Which AI tools did you use?** (if applicable)
   ```
   claude-sonnet-4-6, kimi-k2.5
   ```

3. **What was your level of review?**
   ```
   [1] Glance — brief look
   [2] Moderate review — read and understood
   [3] Substantial modification — significantly changed
   [4] Complete rewrite — AI used as reference only
   [5] None
   ```

4. **How many minutes did you spend on this?**
   ```
   45
   ```

5. **Self-assessed confidence?**
   ```
   high / medium / low
   ```

### Option B: Fast Mode (For Daily Use)

```bash
octp sign --profile fast --yes
```

Uses defaults:
- Method: AI-assisted with substantial review
- Runs: ruff, bandit, detect-secrets (3-8 seconds)

**Output:**
```
Running verification checks...
  ✓ ruff@0.1.15 — No issues found
  ✓ bandit@1.9.4 — No high-severity issues
  ✗ detect-secrets — Secrets found: 2

✓ Envelope signed and written to .octp-envelope.json
```

## Step 5: Verify Your Envelope

```bash
octp verify .octp-envelope.json
```

**Expected output:**
```
✓ Envelope is valid — signature verified
```

## Step 6: Include with Your PR

Add the envelope to your pull request:

```bash
git add .octp-envelope.json
git commit -m "feat: add new feature with trust envelope

This contribution was AI-assisted with substantial human review.
All verification checks passed."
git push
```

## Example Scenarios

### Scenario 1: Bug Fix (Human Only)

You found and fixed a bug manually:

```bash
octp sign
# Select: [1] Human only
# Review level: [3] Substantial modification
# Time: 30 minutes
# Confidence: high
```

**Result:**
```json
{
  "provenance": {
    "method": "human_only",
    "human_review_level": "substantial_modification",
    "human_review_duration_minutes": 30
  }
}
```

### Scenario 2: Refactoring (AI-Assisted)

You used Claude to refactor a module, then reviewed carefully:

```bash
octp sign
# Select: [2] AI assisted, human reviewed
# AI tools: claude-sonnet-4-6
# Review level: [3] Substantial modification
# Time: 60 minutes
# Confidence: medium
```

**Result:**
```json
{
  "provenance": {
    "method": "ai_assisted_human_reviewed",
    "ai_tools": [{
      "model": "claude-sonnet-4-6",
      "vendor": "anthropic",
      "version": "20260215",
      "usage_type": "refactoring"
    }],
    "human_review_level": "substantial_modification",
    "human_review_duration_minutes": 60
  }
}
```

### Scenario 3: Documentation Update (Quick)

You updated docs with minimal review:

```bash
octp sign --profile fast --yes
# Then manually edit .octp-envelope.json to set:
# method: human_only
# review_level: glance
```

## What to Expect

### File Created

`.octp-envelope.json` is created in your repository root. It contains:

- **Header**: Unique ID, timestamp, commit hash
- **Provenance**: How the code was created
- **Verification**: Results of automated checks
- **Integrity**: Cryptographic signature

### Verification Checks Run

Depending on your profile:

- **ruff**: Python linting
- **bandit**: Security scanning
- **detect-secrets**: Secret detection
- **pytest**: Test suite
- **pip-audit**: Dependency vulnerabilities
- **mypy**: Type checking
- **semgrep**: Advanced static analysis

### Time Required

- **Fast profile**: 3-8 seconds
- **CI profile**: 30-60 seconds
- **Full profile**: 2-4 minutes

## Troubleshooting

### "Not inside a git repository"

```bash
# Initialize git first
git init
git add .
git commit -m "Initial commit"

# Then run octp sign
octp sign
```

### "No verification tools installed"

Install the tools for your chosen profile:

```bash
# Fast profile minimum
pip install ruff bandit detect-secrets
```

### Envelope shows "✗ failed" for tests

This means:
1. You selected a profile that includes tests (ci or full)
2. Your test suite has failing tests
3. OR: You selected fast profile which skips tests (shows ○ skipped)

To fix:
```bash
# Run tests first
pytest

# Fix any failures
# Then regenerate envelope
octp sign --profile ci --yes
```

## Next Steps

- [Learn about runner profiles](profiles.md)
- [Configure .octp.toml](configuration.md)
- [Set up CI/CD integration](ci-integration.md)
- [Read the full specification](https://github.com/openoctp/spec)