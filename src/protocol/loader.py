from pathlib import Path

from src.config.loader import load_yaml
from src.models.protocol import Protocol, Section, TestDefinition


def load_protocol(path: str | Path) -> Protocol:
    """Load protocol YAML."""

    data = load_yaml(path)

    sections = []

    for section_data in data["sections"]:

        tests = []

        for test in section_data["tests"]:

            tests.append(
                TestDefinition(
                    key=test["key"],
                    name=test["name"],
                    description=test.get("description") or "",
                    type=test["type"],
                    unit=test.get("unit", ""),

                    tolerance=test.get("tolerance"),
                    tolerance_source=test.get("tolerance_source"),

                    reference=test.get("reference"),
                    reference_source=test.get("reference_source"),

                    baseline=test.get("baseline"),
                    baseline_source=test.get("baseline_source"),

                    trend=test.get("trend", False),
                )
            )

        sections.append(
            Section(
                key=section_data["key"],
                name=section_data["name"],
                tests=tests,
            )
        )

    return Protocol(
        name=data["name"],
        category=data["category"],
        protocol=data["protocol"],
        machine=data["machine"],
        frequency=data["frequency"],
        guideline=data["guideline"],
        sections=sections,
    )