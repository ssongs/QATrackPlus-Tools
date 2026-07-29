from dataclasses import dataclass, field
from datetime import date

from src.models.qa_test import QATest


@dataclass
class QARecord:
    """One QA session."""

    machine: str

    protocol: str

    performed_date: date

    tests: list[QATest] = field(default_factory=list)

    def add_test(self, test: QATest):

        self.tests.append(test)

    @property
    def passed(self):

        return all(test.passed for test in self.tests)