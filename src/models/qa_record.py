from dataclasses import dataclass, field

from src.models.qa_test import QATest


@dataclass
class QARecord:
    """Represents a complete QA record."""

    machine: str
    protocol: str
    tests: list[QATest] = field(default_factory=list)

    def add_test(self, test: QATest) -> None:
        """Add a QA test result."""
        self.tests.append(test)

    @property
    def status(self) -> str:
        """Return overall QA status."""

        if any(test.skipped for test in self.tests):
            if any(
                not test.skipped and not test.passed
                for test in self.tests
            ):
                return "FAIL"

            return "INCOMPLETE"

        if all(test.passed for test in self.tests):
            return "PASS"

        return "FAIL"

    @property
    def passed(self) -> bool:
        """Return True only when the entire QA record passes."""

        return self.status == "PASS"