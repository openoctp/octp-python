# CI/CD Integration

Integrate OCTP into your continuous integration pipelines.

## GitHub Actions

### Basic Workflow

Create `.github/workflows/octp.yml`:

```yaml
name: OCTP Verification

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

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
          echo "✓ Envelope found"

      - name: Install verification tools
        run: |
          pip install ruff bandit detect-secrets pytest pip-audit

      - name: Verify envelope signature
        run: octp verify .octp-envelope.json

      - name: Regenerate and compare
        run: |
          # Regenerate to ensure current state matches
          octp sign --profile ci --yes -o /tmp/new-envelope.json
          
          # Compare key fields (optional strict check)
          # This ensures the committed envelope matches current code
```

### Strict Verification (Recommended)

```yaml
name: OCTP Strict Verification

on:
  pull_request:
    branches: [main]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install octp-python
          pip install ruff bandit detect-secrets pytest pip-audit

      - name: Verify envelope exists
        run: |
          if [ ! -f .octp-envelope.json ]; then
            echo "::error::No OCTP envelope found. Run: octp sign --profile ci --yes"
            exit 1
          fi

      - name: Verify signature
        run: octp verify .octp-envelope.json

      - name: Check test results
        run: |
          # Extract test status from envelope
          TESTS_PASSED=$(cat .octp-envelope.json | jq -r '.verification.tests_passed')
          if [ "$TESTS_PASSED" != "true" ]; then
            echo "::warning::Tests did not pass in envelope"
          fi

      - name: Check provenance method
        run: |
          METHOD=$(cat .octp-envelope.json | jq -r '.provenance.method')
          echo "Provenance method: $METHOD"
          
          # Reject unreviewed AI (optional)
          if [ "$METHOD" = "ai_generated_unreviewed" ]; then
            echo "::error::Unreviewed AI code not accepted"
            exit 1
          fi
```

### Comment on PR

```yaml
name: OCTP PR Comment

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  comment:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: actions/checkout@v4

      - name: Check envelope
        id: check
        run: |
          if [ -f .octp-envelope.json ]; then
            echo "exists=true" >> $GITHUB_OUTPUT
            METHOD=$(jq -r '.provenance.method' .octp-envelope.json)
            echo "method=$METHOD" >> $GITHUB_OUTPUT
          else
            echo "exists=false" >> $GITHUB_OUTPUT
          fi

      - name: Comment on PR
        if: steps.check.outputs.exists == 'true'
        uses: actions/github-script@v7
        with:
          script: |
            const method = '${{ steps.check.outputs.method }}';
            const emoji = method.includes('ai') ? '🤖' : '👤';
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `${emoji} **OCTP Envelope Detected**\n\n` +
                    `Provenance: ${method}\n\n` +
                    `All verification checks included.`
            });
```

## GitLab CI

Create `.gitlab-ci.yml`:

```yaml
stages:
  - verify

octp:verify:
  stage: verify
  image: python:3.11
  before_script:
    - pip install octp-python
    - pip install ruff bandit detect-secrets pytest pip-audit
  script:
    - |
      if [ ! -f .octp-envelope.json ]; then
        echo "No OCTP envelope found"
        exit 1
      fi
    - octp verify .octp-envelope.json
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

## Jenkins

Create `Jenkinsfile`:

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.11'
        }
    }
    stages {
        stage('OCTP Verify') {
            steps {
                sh '''
                    pip install octp-python
                    pip install ruff bandit detect-secrets pytest pip-audit
                    
                    if [ ! -f .octp-envelope.json ]; then
                        echo "No envelope found"
                        exit 1
                    fi
                    
                    octp verify .octp-envelope.json
                '''
            }
        }
    }
}
```

## CircleCI

Create `.circleci/config.yml`:

```yaml
version: 2.1

jobs:
  verify:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - run:
          name: Install OCTP
          command: |
            pip install octp-python
            pip install ruff bandit detect-secrets pytest pip-audit
      - run:
          name: Verify Envelope
          command: |
            if [ ! -f .octp-envelope.json ]; then
              echo "No envelope found"
              exit 1
            fi
            octp verify .octp-envelope.json

workflows:
  verify:
    jobs:
      - verify
```

## Azure DevOps

Create `azure-pipelines.yml`:

```yaml
trigger:
  - main

pr:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'
  displayName: 'Use Python 3.11'

- script: |
    pip install octp-python
    pip install ruff bandit detect-secrets pytest pip-audit
  displayName: 'Install OCTP'

- script: |
    if [ ! -f .octp-envelope.json ]; then
      echo "No envelope found"
      exit 1
    fi
    octp verify .octp-envelope.json
  displayName: 'Verify OCTP Envelope'
```

## Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: octp-verify
        name: Verify OCTP Envelope
        entry: octp verify .octp-envelope.json
        language: system
        pass_filenames: false
        always_run: true
        stages: [commit]
```

## Advanced Patterns

### Envelope Generation in CI

Some teams prefer generating envelopes in CI:

```yaml
- name: Generate envelope in CI
  run: |
    # Use CI-specific profile
    octp sign --profile ci --yes
    
    # Commit back to PR (requires special permissions)
    git add .octp-envelope.json
    git commit -m "chore: update OCTP envelope [ci skip]"
    git push
```

**Warning:** This approach loses the developer's provenance declaration.

### Multi-Repository Projects

For monorepos with multiple packages:

```yaml
- name: Verify all packages
  run: |
    for pkg in packages/*/; do
      if [ -f "$pkg/.octp-envelope.json" ]; then
        echo "Verifying $pkg"
        (cd $pkg && octp verify .octp-envelope.json)
      fi
    done
```

### Matrix Testing

Test with multiple Python versions:

```yaml
strategy:
  matrix:
    python-version: ['3.11', '3.12']

steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
  - run: pip install octp-python
  - run: octp verify .octp-envelope.json
```

## Best Practices

1. **Fail on missing envelope** — Require envelope for all PRs
2. **Verify signature** — Always run `octp verify`
3. **Install tools** — Ensure all runners are available in CI
4. **Cache dependencies** — Speed up subsequent runs
5. **Comment on PRs** — Help contributors understand requirements

## Troubleshooting CI

### "Command not found: octp"

```yaml
# Add to PATH or use python -m
- run: python -m pip install octp-python
- run: python -m octp.cli.main --help
```

### Timeouts in CI

```yaml
# Increase timeout for slow runners
- run: |
    timeout 300 octp sign --profile ci --yes || true
```

### Tool Installation Failures

```yaml
# Install tools individually with error handling
- run: |
    pip install ruff || echo "ruff install failed"
    pip install bandit || echo "bandit install failed"
    # Continue with available tools
```

## See Also

- [Configuration Guide](configuration.md)
- [Runner Profiles](profiles.md)
- [Quick Start](quickstart.md)