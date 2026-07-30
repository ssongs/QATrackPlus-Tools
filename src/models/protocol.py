from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TestDefinition:
    """Definition of a QA test loaded from a protocol."""

    key: str
    name: str
    type: str

    unit: str = ""

    tolerance: Optional[float] = None
    reference: Optional[float] = None
    baseline: Optional[float] = None

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

    sections: list[Section] = field(default_factory=list)