# Installation Guide

## Requirements

- Python 3.11 or higher
- Git repository (OCTP reads git metadata)

## Standard Installation

```bash
pip install octp-python
```

## Development Installation

For contributing or running from source:

```bash
git clone https://github.com/openoctp/octp-python
cd octp-python
pip install -e ".[dev]"
```

## Verification

Verify installation:

```bash
octp --help
```

Expected output:
```
Usage: octp [OPTIONS] COMMAND [ARGS]...

Open Contribution Trust Protocol — generate and verify trust envelopes

Options:
  --help  Show this message and exit.

Commands:
  init    Initialise OCTP in a repository — creates .octp.toml
  sign    Generate and sign a trust envelope for the current commit
  verify  Verify a trust envelope — check integrity and signature
```

## Optional Dependencies

For full functionality, install these verification tools:

```bash
# Core tools (fast profile)
pip install ruff bandit detect-secrets

# Extended tools (ci profile)
pip install pytest pip-audit

# Full suite (full profile)
pip install mypy semgrep
```

Or install all at once:

```bash
pip install ruff bandit detect-secrets pytest pip-audit mypy semgrep
```

## Platform-Specific Notes

### macOS

```bash
# Using Homebrew for system dependencies
brew install git

# Then install octp-python
pip install octp-python
```

### Linux (Ubuntu/Debian)

```bash
# Ensure git is installed
sudo apt-get update
sudo apt-get install git

# Install octp-python
pip install octp-python
```

### Windows

```powershell
# Install via pip (requires Python 3.11+)
pip install octp-python

# Git must be installed and in PATH
# Download from: https://git-scm.com/download/win
```

## Troubleshooting

### "command not found: octp"

Your Python scripts directory isn't in PATH:

```bash
# Find where pip installed it
which python
# Add the bin directory to PATH
export PATH="$PATH:$(python -m site --user-base)/bin"
```

Or use Python module syntax:

```bash
python -m octp.cli.main --help
```

### Import errors after installation

Try reinstalling:

```bash
pip uninstall octp-python
pip install --no-cache-dir octp-python
```

## Next Steps

- [Quick Start Guide](quickstart.md)
- [Configuration Reference](configuration.md)
- [Runner Profiles](profiles.md)