from __future__ import annotations
import shutil
import subprocess
from .base import CheckRunner, CheckResult


class DepsRunner(CheckRunner):
    name = "pip-audit"

    def is_available(self) -> bool:
        return shutil.which("pip-audit") is not None

    def run(self, repo_root: str) -> CheckResult:
        try:
            result = subprocess.run(
                ["pip-audit", "--progress-spinner=off"],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=60,
            )
            passed = result.returncode == 0
            detail = "No known vulnerabilities" if passed else result.stdout[:200]
        except subprocess.TimeoutExpired:
            passed = False
            detail = "pip-audit timed out"
        except Exception as e:
            passed = False
            detail = f"Runner error: {e}"

        return CheckResult(
            passed=passed,
            tool_name="pip-audit",
            suite_hash=None,
            detail=detail,
        )
