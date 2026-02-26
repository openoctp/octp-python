from __future__ import annotations
import shutil
import subprocess
from .base import CheckRunner, CheckResult


class RuffRunner(CheckRunner):
    name = "ruff"

    def is_available(self) -> bool:
        return shutil.which("ruff") is not None

    def run(self, repo_root: str) -> CheckResult:
        try:
            result = subprocess.run(
                ["ruff", "check", "."],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=60,
            )
            passed = result.returncode == 0
            detail = "No issues found" if passed else result.stdout[:200]
        except subprocess.TimeoutExpired:
            passed = False
            detail = "Ruff timed out after 60 seconds"
        except Exception as e:
            passed = False
            detail = f"Runner error: {e}"

        try:
            v = subprocess.run(["ruff", "--version"], capture_output=True, text=True)
            version = v.stdout.strip().split(" ")[1] if v.stdout else "unknown"
        except Exception:
            version = "unknown"

        return CheckResult(
            passed=passed,
            tool_name=f"ruff@{version}",
            suite_hash=None,
            detail=detail,
        )
