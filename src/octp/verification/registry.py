from __future__ import annotations

from pathlib import Path

from .bandit_runner import BanditRunner
from .base import CheckResult, CheckRunner
from .deps_runner import DepsRunner
from .detect_secrets_runner import DetectSecretsRunner
from .mypy_runner import MypyRunner
from .pytest_runner import PytestRunner
from .ruff_runner import RuffRunner
from .semgrep_runner import SemgrepRunner

# Define runner profiles - choose smartest combinations
RUNNER_PROFILES = {
    "full": [  # All checks - comprehensive but slower
        PytestRunner,
        RuffRunner,
        MypyRunner,
        SemgrepRunner,
        BanditRunner,
        DepsRunner,
        DetectSecretsRunner,
    ],
    "fast": [  # Essential checks only - 3-8 seconds
        RuffRunner,  # Fast linting (Rust-based)
        BanditRunner,  # Python security
        DetectSecretsRunner,  # Secret detection
    ],
    "ci": [  # CI/CD optimized - good balance
        PytestRunner,
        RuffRunner,
        BanditRunner,
        DepsRunner,
        DetectSecretsRunner,
    ],
    "security": [  # Security focused
        BanditRunner,
        DepsRunner,
        DetectSecretsRunner,
        SemgrepRunner,
    ],
}

# Default runners if no profile specified
DEFAULT_PROFILE = "full"


def get_runners_for_profile(profile: str) -> list[type[CheckRunner]]:
    """Get runner classes for a named profile."""
    if profile not in RUNNER_PROFILES:
        raise ValueError(
            f"Unknown profile: {profile}. "
            f"Available: {', '.join(RUNNER_PROFILES.keys())}"
        )
    return RUNNER_PROFILES[profile]


def get_available_runners(
    repo_root: Path,
    profile: str = DEFAULT_PROFILE,
    runner_names: list[str] | None = None,
) -> list[CheckRunner]:
    """Return available runners matching the profile or specific names.

    Args:
        repo_root: Path to the repository
        profile: Runner profile name ('fast', 'full', 'ci', 'security')
        runner_names: Optional list of specific runner names to use instead of profile
    """
    if runner_names:
        # Use specific runners
        runner_classes = [
            cls for cls in RUNNER_PROFILES["full"] if cls.name in runner_names
        ]
    else:
        # Use profile
        runner_classes = get_runners_for_profile(profile)

    available = []
    for RunnerClass in runner_classes:
        runner = RunnerClass()
        if runner.is_available():
            available.append(runner)

    return available


def run_all(
    repo_root: Path,
    profile: str = DEFAULT_PROFILE,
    runner_names: list[str] | None = None,
    max_workers: int = 4,
) -> dict[str, CheckResult]:
    """Run all available checks and return results keyed by runner name.

    Args:
        repo_root: Path to the repository
        profile: Runner profile name
        runner_names: Optional specific runner names to use
        max_workers: Maximum parallel workers

    Returns:
        Dictionary mapping runner names to their results
    """
    import concurrent.futures

    runners = get_available_runners(repo_root, profile, runner_names)
    results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all runners
        future_to_runner = {
            executor.submit(runner.run, str(repo_root)): runner for runner in runners
        }

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_runner):
            runner = future_to_runner[future]
            try:
                results[runner.name] = future.result()
            except Exception as e:
                results[runner.name] = CheckResult(
                    passed=False,
                    tool_name=runner.name,
                    suite_hash=None,
                    detail=f"Runner crashed: {e}",
                )

    return results
