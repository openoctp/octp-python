# Troubleshooting Guide

Common issues and their solutions.

## Installation Issues

### "pip install octp-python" fails

**Problem:** Package not found or installation errors.

**Solutions:**

```bash
# Update pip first
pip install --upgrade pip

# Install with verbose output to see errors
pip install -v octp-python

# Try without cache
pip install --no-cache-dir octp-python

# Check Python version (requires 3.11+)
python --version
```

### "command not found: octp"

**Problem:** The `octp` command isn't in your PATH.

**Solutions:**

```bash
# Find where pip installed it
which python
ls $(python -m site --user-base)/bin/

# Add to PATH (temporary)
export PATH="$PATH:$(python -m site --user-base)/bin"

# Add to PATH (permanent - add to ~/.bashrc or ~/.zshrc)
echo 'export PATH="$PATH:$(python -m site --user-base)/bin"' >> ~/.bashrc
source ~/.bashrc

# Or use Python module syntax
python -m octp.cli.main --help
```

### Import errors after installation

**Problem:** Module not found when running octp.

**Solution:**

```bash
# Reinstall with force
pip uninstall octp-python -y
pip install --force-reinstall octp-python

# Check if multiple Python versions conflict
which python3
which python
pip --version  # Should match your python version
```

## Runtime Issues

### "Not inside a git repository"

**Problem:** OCTP requires a git repository.

**Solution:**

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"

# Then run octp
octp sign
```

### "No verification tools installed"

**Problem:** The runners need external tools installed.

**Solution:**

```bash
# Install minimum for fast profile
pip install ruff bandit detect-secrets

# Or install all
pip install ruff bandit detect-secrets pytest pip-audit mypy semgrep
```

### "pip-audit timed out"

**Problem:** Network issues or slow connection.

**Solutions:**

```bash
# Use fast profile (skips pip-audit)
octp sign --profile fast --yes

# Increase timeout (if using custom scripts)
timeout 300 octp sign --profile ci --yes

# Check network connectivity
pip-audit --progress-spinner=off
```

### "semgrep timed out"

**Problem:** Semgrep downloads rules on first run.

**Solutions:**

```bash
# First run is slow - rules are cached for 24 hours
# Just wait, subsequent runs will be faster

# Use profile without semgrep
octp sign --profile ci --yes

# Pre-download rules
semgrep --config=auto --dry-run
```

### Tests show "✗ failed" but my tests pass

**Problem:** Confusion between "failed" and "skipped".

**Clarification:**

- **✓ passed** — Tests ran and passed
- **✗ failed** — Tests ran and failed  
- **○ skipped** — Tests not run (fast profile skips tests)

**Solution:**

```bash
# If using fast profile, tests are skipped (○ skipped)
# Switch to ci or full profile to run tests
octp sign --profile ci --yes
```

### Interactive prompts crash in CI/CD

**Problem:** Non-interactive environment can't handle prompts.

**Solution:**

```bash
# Always use --yes in automation
octp sign --profile ci --yes

# Or pipe empty input
echo "" | octp sign --profile ci
```

## Verification Issues

### "Envelope is INVALID — payload hash mismatch"

**Problem:** The envelope was modified after signing.

**Solutions:**

```bash
# Regenerate the envelope
octp sign --profile ci --yes

# Don't manually edit .octp-envelope.json
# Always regenerate using octp sign
```

### "No integrity section found"

**Problem:** Envelope wasn't signed.

**Solution:**

```bash
# Re-run with signing
octp sign --profile ci --yes

# Check the envelope has integrity section
jq '.integrity' .octp-envelope.json
```

### "Could not parse envelope"

**Problem:** JSON is malformed.

**Solution:**

```bash
# Validate JSON
jq '.' .octp-envelope.json

# If invalid, regenerate
rm .octp-envelope.json
octp sign --profile ci --yes
```

## Profile Issues

### Fast profile is still slow

**Problem:** Even fast profile taking too long.

**Possible causes:**

1. **First run:** Initial setup takes time
2. **Large repository:** Scanning many files
3. **Slow disk:** I/O bound operations

**Solutions:**

```bash
# Check what's slow
time octp sign --profile fast --yes

# Exclude directories (future feature)
# For now, move large non-code directories out of repo

# Use timeout to see if it's hanging
timeout 30 octp sign --profile fast --yes || echo "Timed out"
```

### Full profile times out

**Problem:** Full profile takes too long on slow machines.

**Solutions:**

```bash
# Use CI profile instead (good balance)
octp sign --profile ci --yes

# Or fast profile for daily work
octp sign --profile fast --yes

# Run full profile only for releases
```

## Git Issues

### "Invalid git repository"

**Problem:** Current directory isn't a git repo or is corrupted.

**Solutions:**

```bash
# Check if .git exists
ls -la .git

# Check git status
git status

# Reinitialize if needed
git init
```

### "Could not parse remote URL"

**Problem:** Git remote URL format not recognized.

**Current supported formats:**
- `git@github.com:user/repo.git`
- `https://github.com/user/repo.git`

**Workaround:**

The envelope will show "unknown/unknown/unknown" but will still work.

## Configuration Issues

### ".octp.toml not found"

**Problem:** Configuration file missing.

**Solution:**

```bash
# Generate default config
octp init

# Or create manually
cat > .octp.toml << 'EOF'
[policy]
require_envelope = true
minimum_review_level = "moderate_review"

[runners]
default_profile = "ci"
test_runner = "pytest"
linting = "ruff"
EOF
```

### Changes to .octp.toml not taking effect

**Problem:** OCTP caches or doesn't reload config.

**Solution:**

Config is read fresh each run. If changes aren't working:

```bash
# Check file syntax
cat .octp.toml

# Validate TOML
python -c "import tomllib; print(tomllib.load(open('.octp.toml', 'rb')))"
```

## Performance Issues

### Envelope generation is slow

**Benchmark your setup:**

```bash
# Time each profile
echo "Fast profile:"
time octp sign --profile fast --yes

echo "CI profile:"
time octp sign --profile ci --yes

echo "Full profile:"
time octp sign --profile full --yes
```

**Expected times:**
- Fast: 3-10 seconds
- CI: 30-90 seconds
- Full: 2-5 minutes

**If much slower:**

1. Check available tools: `which ruff bandit detect-secrets`
2. Network issues (pip-audit, safety hit network)
3. First-run setup (semgrep downloads rules)

### Parallel execution not helping

**Problem:** Expected speedup from parallel runners not seen.

**Note:** Parallel execution helps most when:
- Multiple slow runners are available
- Machine has multiple CPU cores
- Not I/O bound

**Current single-threaded runners:** pytest (tests are sequential)

## Getting Help

### Check version

```bash
octp --help | head -5
```

### Check installation

```bash
python -c "import octp; print(octp.__version__)"
```

### Debug mode

```bash
# Verbose output (if implemented)
octp sign --verbose

# Or check logs
OCTP_DEBUG=1 octp sign --profile ci --yes
```

### Report issues

Include:
1. OCTP version: `python -c "import octp; print(octp.__version__)"`
2. Python version: `python --version`
3. OS: `uname -a`
4. Error message (full traceback)
5. Command run: `octp sign --profile ci --yes`
6. Profile used: fast/ci/full

**Report at:** https://github.com/openoctp/octp-python/issues

## Known Limitations

1. **No Windows support** — Not tested on Windows
2. **Python 3.11+ only** — Older versions not supported
3. **Git required** — No support for other VCS
4. **Network dependent** — pip-audit and safety require internet
5. **First run slow** — semgrep downloads rules initially

## See Also

- [Installation Guide](installation.md)
- [Quick Start](quickstart.md)
- [Configuration Reference](configuration.md)