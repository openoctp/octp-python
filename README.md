# octp

**Open Contribution Trust Protocol — Python reference implementation**

Generate and verify cryptographically signed trust envelopes 
for your open source contributions.

## Install
```bash
pip install octp
```

## Usage
```bash
# In any git repository, before submitting a PR
octp sign

# Verify an incoming envelope
octp verify path/to/envelope.json
```

## Status

v0.1.0 — Early development. Spec: OCTP v0.1

## Links

→ [Specification](https://github.com/octp/spec)  
→ [Documentation](docs/)  
→ [Contributing](CONTRIBUTING.md)
```

Commit to main. Message: `Initial README`.

---

**Repository 3: website**

Back to `github.com/octp`. Click "New repository."
```
Repository name:     website
Description:         Source for octp.dev
Visibility:          Public
Initialize with:     README (check this)
Add .gitignore:      Node
Choose a license:    MIT License
```

Click "Create repository."

Leave the README as is for now. You'll build this properly later.

---

**Repository 4: community**

Back to `github.com/octp`. Click "New repository."
```
Repository name:     community
Description:         RFCs, governance, discussions, and adopters list
Visibility:          Public
Initialize with:     README (check this)
Add .gitignore:      None
Choose a license:    Creative Commons Attribution 4.0 International
