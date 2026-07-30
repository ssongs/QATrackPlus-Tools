from datetime import date

from src.models.protocol import Protocol
from src.models.qa_record import QARecord
from src.models.qa_test import QATest


def build_record(
    protocol: Protocol,
    results: dict,
    machine: str | None = None,
    performed_date: date | None = None,
) -> QARecord:
    """Build a QARecord from a protocol and result dictionary."""

    record = QARecord(
        machine=machine or protocol.name,
        protocol=protocol.protocol,
        performed_date=performed_date or date.today(),
    )

    for section in protocol.sections:
        for test in section.tests:

            record.add_test(
                QATest(
                    key=test.key,
                    name=test.name,
                    test_type=test.type,
                    result=results.get(test.key),
                    unit=test.unit,
                    tolerance=test.tolerance,
                    reference=test.reference,
                    baseline=test.baseline,
                    trend=test.trend,
                )
            )

    return record