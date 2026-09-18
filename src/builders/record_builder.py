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


def build_records(
    protocol: Protocol,
    results: dict,
    machine: str | None = None,
) -> dict[str, QARecord]:
    """Build QARecords grouped by measurement date."""

    dates = sorted({
        result["date"][:10]
        for test_results in results.values()
        for result in test_results
    })

    records = {}

    for target_date in dates:
        daily_results = {}

        for key, test_results in results.items():
            result = next(
                (
                    item
                    for item in test_results
                    if item["date"][:10] == target_date
                ),
                None,
            )

            if result is None:
                daily_results[key] = {
                    "result": None,
                    "skipped": True,
                    "comment": "",
                }
            else:
                daily_results[key] = {
                    "result": result["value"],
                    "skipped": result["skipped"],
                    "comment": result["comment"],
                }

        records[target_date] = build_record(
            protocol,
            daily_results,
            machine=machine,
        )

    return records