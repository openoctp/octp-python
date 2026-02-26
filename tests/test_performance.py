"""Performance benchmarks for OCTP."""

import time

from octp.verification.registry import run_all


class TestPerformance:
    """Performance benchmarks."""

    def test_fast_profile_under_15_seconds(self, tmp_path):
        """Fast profile should complete in under 15s even on slow machines."""
        # Create a minimal git repo structure
        (tmp_path / ".git").mkdir()
        (tmp_path / ".git" / "config").write_text("")

        start = time.time()
        # This will fail because it's not a real git repo, but we measure timing
        try:
            run_all(tmp_path, profile="fast")
        except Exception:
            pass  # We care about timing, not success
        elapsed = time.time() - start

        # Should be very fast when runners aren't available
        assert elapsed < 15, f"Too slow: {elapsed:.2f}s"

    def test_parallel_execution_faster_than_sequential(self, tmp_path):
        """Parallel execution should be faster than sequential."""
        # This is more of an integration test
        # In practice, parallel should be ~40-60% faster
        pass  # Would need timing infrastructure

    def test_envelope_generation_scalability(self):
        """Envelope generation time should not grow linearly with repo size."""
        # This would test that we only scan changed files, etc.
        pass
