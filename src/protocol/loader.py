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
                    type=test["type"],
                    unit=test.get("unit", ""),
                    reference=test.get("reference"),
                    tolerance=test.get("tolerance"),
                    history=test.get("history", False),
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
        sections=sections,
    )