from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TestDefinition:
    """Definition of a QA test loaded from a protocol."""

    key: str
    name: str
    description: str
    type: str
    unit: str = ""

    tolerance: Optional[float] = None
    tolerance_source: Optional[str] = None
    reference: Optional[float] = None
    reference_source: Optional[str] = None
    baseline: Optional[float] = None
    baseline_source: Optional[str] = None

    trend: bool = False


@dataclass
class Section:
    """A section within a QA protocol."""

    key: str
    name: str
    tests: list[TestDefinition] = field(default_factory=list)


@dataclass
class Protocol:
    """QA protocol."""

    name: str
    category: str
    protocol: str

    machine: dict
    frequency: str
    guideline: list[str]

    sections: list[Section] = field(default_factory=list)