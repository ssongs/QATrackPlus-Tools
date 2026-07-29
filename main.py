from datetime import date

from src.models.qa_record import QARecord
from src.models.qa_test import QATest


record = QARecord(
    machine="Siemens go.Sim",
    protocol="CT Daily QA",
    performed_date=date.today(),
)

record.add_test(
    QATest(
        key="laser",
        name="Gantry / Moving Laser",
        test_type="boolean",
        result=True,
    )
)

record.add_test(
    QATest(
        key="hu_water",
        name="HU Water",
        test_type="numeric",
        result=2,
        reference=0,
        tolerance=5,
        unit="HU",
        trend=True,
    )
)

print(record)
print(record.passed)