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

    reference: Optional[float] = None

    tolerance: Optional[float] = None

    trend: bool = False

    @property
    def passed(self) -> bool:
        """Return True if the test passes."""

        if self.test_type == "boolean":
            return bool(self.result)

        if self.reference is None or self.tolerance is None:
            return False

        return abs(float(self.result) - self.reference) <= self.tolerance