from dataclasses import dataclass
from typing import Optional


@dataclass
class QATest:
    """Represents a single QA test item."""

    key: str
    name: str

    test_type: str  # "boolean" or "numeric"

    result: bool | float | None

    skipped: bool = False
    comment: str=""

    unit: str = ""

    tolerance: Optional[float] = None
    reference: Optional[float] = None

    trend: bool = False

    @property
    def passed(self) -> bool:
        """Return True if the test passes."""

        if self.skipped:
            return False

        if self.result is None:
            return False

        if self.test_type == "boolean":
            return bool(self.result)

        if self.tolerance is None:
            return False

        if self.reference is None:
            return False

        return abs(float(self.result) - self.reference) <= self.tolerance