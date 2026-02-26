from __future__ import annotations
from pathlib import Path
from .base import CheckRunner, CheckResult
from .pytest_runner import PytestRunner
from .semgrep_runner import SemgrepRunner
from .bandit_runner import BanditRunner
from .deps_runner import DepsRunner


ALL_RUNNERS: list[type[CheckRunner]] = [
    PytestRunner,
    SemgrepRunner,
    BanditRunner,
    DepsRunner,
]


def get_available_runners(repo_root: Path) -> list[CheckRunner]:
    """Return all runners that are available in this environment."""
    available = []
    for RunnerClass in ALL_RUNNERS:
        runner = RunnerClass()
        if runner.is_available():
            available.append(runner)
    return available


def run_all(repo_root: Path) -> dict[str, CheckResult]:
    """Run all available checks and return results keyed by runner name."""
    runners = get_available_runners(repo_root)
    results = {}
    for runner in runners:
        results[runner.name] = runner.run(str(repo_root))
    return results
