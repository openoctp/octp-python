from __future__ import annotations
import hashlib
import shutil
import subprocess
from pathlib import Path
from .base import CheckRunner, CheckResult


class PytestRunner(CheckRunner):
    name = "pytest"

    def is_available(self) -> bool:
        return shutil.which("pytest") is not None

    def run(self, repo_root: str) -> CheckResult:
        root = Path(repo_root)

        # Hash the test suite for integrity
        suite_hash = self._hash_tests(root)

        try:
            result = subprocess.run(
                ["pytest", "--tb=no", "-q"],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=120,
            )
            passed = result.returncode == 0
            detail = (
                result.stdout.strip().split("\n")[-1] if result.stdout else "No output"
            )
        except subprocess.TimeoutExpired:
            passed = False
            detail = "Test suite timed out after 120 seconds"
        except Exception as e:
            passed = False
            detail = f"Runner error: {e}"

        # Get pytest version
        try:
            v = subprocess.run(["pytest", "--version"], capture_output=True, text=True)
            version = v.stdout.strip().split(" ")[1] if v.stdout else "unknown"
        except Exception:
            version = "unknown"

        return CheckResult(
            passed=passed,
            tool_name=f"pytest@{version}",
            suite_hash=suite_hash,
            detail=detail,
        )

    def _hash_tests(self, root: Path) -> str | None:
        """Hash all test files for integrity tracking."""
        test_dirs = [root / "tests", root / "test"]
        files = []
        for d in test_dirs:
            if d.exists():
                files.extend(sorted(d.rglob("test_*.py")))
        if not files:
            return None
        h = hashlib.sha256()
        for f in files:
            h.update(f.read_bytes())
        return h.hexdigest()[:32]
