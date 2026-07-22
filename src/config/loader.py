from pathlib import Path
import yaml


def load_yaml(path: str | Path) -> dict:
    """Load a YAML file and return it as a dictionary."""

    path = Path(path)

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)