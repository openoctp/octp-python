from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CheckResult:
    passed: bool
    tool_name: str  # e.g. "pytest@7.4.0"
    suite_hash: str | None  # hash of test suite if applicable
    detail: str  # human-readable summary


class CheckRunner(ABC):
    """Abstract base for all verification runners."""

    name: str = ""  # Class attribute - subclasses override this

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not cls.name:
            raise TypeError(f"{cls.__name__} must define 'name'")

    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if this runner can be used in the current environment."""
        ...

    @abstractmethod
    def run(self, repo_root: str) -> CheckResult:
        """Run the check and return a result."""
        ...
