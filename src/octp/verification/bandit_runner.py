from __future__ import annotations

import shutil
import subprocess

from .base import CheckResult, CheckRunner


class BanditRunner(CheckRunner):
    name = "bandit"

    def is_available(self) -> bool:
        return shutil.which("bandit") is not None

    def run(self, repo_root: str) -> CheckResult:
        try:
            result = subprocess.run(
                ["bandit", "-r", ".", "-q", "-ll"],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=60,
            )
            passed = result.returncode == 0
            detail = "No high-severity issues" if passed else result.stdout[:200]
        except subprocess.TimeoutExpired:
            passed = False
            detail = "Bandit timed out"
        except Exception as e:
            passed = False
            detail = f"Runner error: {e}"

        return CheckResult(
            passed=passed,
            tool_name="bandit",
            suite_hash=None,
            detail=detail,
        )
