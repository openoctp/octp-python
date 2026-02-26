from __future__ import annotations
import shutil
import subprocess
from .base import CheckRunner, CheckResult


class MypyRunner(CheckRunner):
    name = "mypy"

    def is_available(self) -> bool:
        return shutil.which("mypy") is not None

    def run(self, repo_root: str) -> CheckResult:
        try:
            result = subprocess.run(
                ["mypy", "src/"],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=120,
            )
            passed = result.returncode == 0
            detail = "No type errors" if passed else result.stdout[:200]
        except subprocess.TimeoutExpired:
            passed = False
            detail = "MyPy timed out after 120 seconds"
        except Exception as e:
            passed = False
            detail = f"Runner error: {e}"

        try:
            v = subprocess.run(["mypy", "--version"], capture_output=True, text=True)
            version = v.stdout.strip().split(" ")[1] if v.stdout else "unknown"
        except Exception:
            version = "unknown"

        return CheckResult(
            passed=passed,
            tool_name=f"mypy@{version}",
            suite_hash=None,
            detail=detail,
        )
