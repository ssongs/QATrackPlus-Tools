from dataclasses import dataclass, field
from datetime import date

from src.models.qa_test import QATest


@dataclass
class QARecord:
    """Represents a QA record."""

    machine: str
    protocol: str
    performed_date: date

    tests: list[QATest] = field(default_factory=list)

    def add_test(self, test: QATest) -> None:
        """Add a QA test to the record."""

        self.tests.append(test)

    @property
    def passed(self) -> bool:
        """Return True if all QA tests pass."""

        return all(test.passed for test in self.tests)