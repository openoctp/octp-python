from __future__ import annotations

import shutil
import subprocess

from .base import CheckResult, CheckRunner


class DetectSecretsRunner(CheckRunner):
    name = "detect-secrets"

    def is_available(self) -> bool:
        return shutil.which("detect-secrets") is not None

    def run(self, repo_root: str) -> CheckResult:
        try:
            result = subprocess.run(
                ["detect-secrets", "scan", "."],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=60,
            )
            passed = result.returncode == 0
            # detect-secrets scan outputs JSON to stdout, errors to stderr
            import json

            try:
                scan_result = json.loads(result.stdout)
                has_secrets = len(scan_result.get("results", {})) > 0
                passed = not has_secrets
                detail = (
                    "No secrets detected"
                    if passed
                    else f"Secrets found: {len(scan_result.get('results', {}))}"
                )
            except json.JSONDecodeError:
                detail = "Scan completed" if passed else "Potential secrets detected"
        except subprocess.TimeoutExpired:
            passed = False
            detail = "detect-secrets timed out after 60 seconds"
        except Exception as e:
            passed = False
            detail = f"Runner error: {e}"

        return CheckResult(
            passed=passed,
            tool_name="detect-secrets",
            suite_hash=None,
            detail=detail,
        )
