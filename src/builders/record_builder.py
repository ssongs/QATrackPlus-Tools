from datetime import date

from src.models.protocol import Protocol
from src.models.qa_record import QARecord
from src.models.qa_test import QATest


def build_record(
    protocol: Protocol,
    results: dict,
    machine: str | None = None,
) -> QARecord:
    """Build a QARecord from a protocol and result dictionary."""

    record = QARecord(
        machine=machine or protocol.name,
        protocol=protocol.protocol,
    )

    for section in protocol.sections:
        for test in section.tests:

            result_data = results.get(test.key, {})

            record.add_test(
                QATest(
                    key=test.key,
                    name=test.name,
                    test_type=test.type,
                    result=result_data.get("result"),
                    skipped=result_data.get("skipped", False),
                    comment=result_data.get("comment", ""),
                    unit=test.unit,
                    tolerance=test.tolerance,
                    reference=test.reference,
                    trend=test.trend,
                )
            )

    return record