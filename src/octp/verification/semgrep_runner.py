from __future__ import annotations

import shutil
import subprocess

from .base import CheckResult, CheckRunner


class SemgrepRunner(CheckRunner):
    name = "semgrep"

    def is_available(self) -> bool:
        return shutil.which("semgrep") is not None

    def run(self, repo_root: str) -> CheckResult:
        try:
            result = subprocess.run(
                ["semgrep", "--config=auto", "--quiet", "--error", "."],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=120,
            )
            passed = result.returncode == 0
            detail = (
                "No issues found" if passed else f"Issues found: {result.stderr[:200]}"
            )
        except subprocess.TimeoutExpired:
            passed = False
            detail = "Semgrep timed out after 120 seconds"
        except Exception as e:
            passed = False
            detail = f"Runner error: {e}"

        try:
            v = subprocess.run(["semgrep", "--version"], capture_output=True, text=True)
            version = v.stdout.strip() if v.stdout else "unknown"
        except Exception:
            version = "unknown"

        return CheckResult(
            passed=passed,
            tool_name=f"semgrep@{version}",
            suite_hash=None,
            detail=detail,
        )
