from dataclasses import dataclass
from typing import Optional


@dataclass
class QATest:
    """Represents a single QA test item."""

    key: str
    name: str

    test_type: str  # "boolean" or "numeric"

    result: bool | float

    unit: str = ""

    tolerance: Optional[float] = None

    reference: Optional[float] = None

    baseline: Optional[float] = None

    trend: bool = False

    @property
    def passed(self) -> bool:
        """Return True if the test passes."""

        if self.test_type == "boolean":
            return bool(self.result)

        if self.tolerance is None:
            return False

        target = self.baseline if self.baseline is not None else self.reference

        if target is None:
            return False

        return abs(float(self.result) - target) <= self.tolerance