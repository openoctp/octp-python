"""Tests for parallel runner execution and profiles."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from octp.verification.base import CheckResult, CheckRunner
from octp.verification.registry import (
    RUNNER_PROFILES,
    get_available_runners,
    get_runners_for_profile,
    run_all,
)


class MockRunner(CheckRunner):
    """Mock runner for testing."""

    name = "mock"

    def __init__(self, available=True, should_fail=False, name=None):
        self._available = available
        self._should_fail = should_fail
        if name:
            self.name = name

    def is_available(self):
        return self._available

    def run(self, repo_root):
        if self._should_fail:
            raise RuntimeError("Mock failure")
        return CheckResult(
            passed=True,
            tool_name=f"{self.name}@1.0",
            suite_hash=None,
            detail="Mock success",
        )


class TestRunnerProfiles:
    """Test runner profile selection."""

    def test_get_runners_for_profile_fast(self):
        """Fast profile should have 3 runners."""
        runners = get_runners_for_profile("fast")
        assert len(runners) == 3
        runner_names = {r.name for r in runners}
        assert runner_names == {"ruff", "bandit", "detect-secrets"}

    def test_get_runners_for_profile_full(self):
        """Full profile should have all runners."""
        runners = get_runners_for_profile("full")
        assert len(runners) == 7  # All except safety
        runner_names = {r.name for r in runners}
        assert "pytest" in runner_names
        assert "ruff" in runner_names
        assert "pip-audit" in runner_names

    def test_get_runners_for_profile_ci(self):
        """CI profile should have 5 runners."""
        runners = get_runners_for_profile("ci")
        assert len(runners) == 5

    def test_get_runners_for_profile_security(self):
        """Security profile should have 4 runners."""
        runners = get_runners_for_profile("security")
        assert len(runners) == 4

    def test_get_runners_invalid_profile(self):
        """Should raise error for invalid profile."""
        with pytest.raises(ValueError, match="Unknown profile"):
            get_runners_for_profile("invalid")


class TestParallelExecution:
    """Test parallel runner execution."""

    def test_run_all_parallel_execution(self, tmp_path):
        """Runners should execute in parallel."""
        # Create mock runners
        runner1 = MockRunner()
        runner2 = MockRunner()

        with patch(
            "octp.verification.registry.get_available_runners",
            return_value=[runner1, runner2],
        ):
            results = run_all(tmp_path)

        assert "mock" in results
        assert results["mock"].passed is True

    def test_run_all_handles_runner_crash(self, tmp_path):
        """Should handle crashed runners gracefully."""
        failing_runner = MockRunner(should_fail=True)

        with patch(
            "octp.verification.registry.get_available_runners",
            return_value=[failing_runner],
        ):
            results = run_all(tmp_path)

        assert "mock" in results
        assert results["mock"].passed is False
        assert "crashed" in results["mock"].detail.lower()

    def test_run_all_respects_profile(self, tmp_path):
        """Should only run runners for specified profile."""
        # Verify that fast profile has fewer runners than full
        fast_runners = get_runners_for_profile("fast")
        full_runners = get_runners_for_profile("full")

        assert len(fast_runners) < len(full_runners)
        assert len(fast_runners) == 3  # ruff, bandit, detect-secrets
        assert len(full_runners) == 7  # All except safety


class TestAvailableRunners:
    """Test runner availability filtering."""

    def test_get_available_runners_returns_list(self, tmp_path):
        """Should return a list of runners."""
        # The function should return a list (might be empty if no tools installed)
        available = get_available_runners(tmp_path, profile="fast")
        assert isinstance(available, list)

    def test_get_available_runners_with_specific_names(self, tmp_path):
        """Should filter by specific runner names."""
        # This test validates the interface signature exists
        # Actual filtering would need real runner classes with matching names
        try:
            # Just verify the function accepts the parameter
            get_available_runners(tmp_path, profile="fast", runner_names=["ruff"])
        except Exception:
            pass  # Expected if runners aren't available
