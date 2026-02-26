from __future__ import annotations

import shutil
import subprocess

from .base import CheckResult, CheckRunner


class SafetyRunner(CheckRunner):
    name = "safety"

    def is_available(self) -> bool:
        return shutil.which("safety") is not None

    def run(self, repo_root: str) -> CheckResult:
        try:
            result = subprocess.run(
                ["safety", "check", "--json"],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=60,
            )
            # Safety returns 0 if no vulnerabilities, 64 if vulnerabilities found
            passed = result.returncode == 0
            detail = "No known vulnerabilities" if passed else "Vulnerabilities found"
        except subprocess.TimeoutExpired:
            passed = False
            detail = "Safety timed out after 60 seconds"
        except Exception as e:
            passed = False
            detail = f"Runner error: {e}"

        return CheckResult(
            passed=passed,
            tool_name="safety",
            suite_hash=None,
            detail=detail,
        )
