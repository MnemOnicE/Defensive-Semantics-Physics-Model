from dataclasses import dataclass, asdict
import json
from typing import Any, Dict

@dataclass
class SPMSignal:
    """
    Represents a core SPM signal as defined in the agent design sketch.

    Attributes:
        concept (str): The name of the concept being monitored.
        mass (float): The semantic mass (Ms) of the concept.
        acceleration (float): The observed or predicted semantic acceleration (As) magnitude.
        ethos (float): The ethos coefficient (eta) of the data source.
        source (str): The identifier of the data source or channel.
    """
    concept: str
    mass: float
    acceleration: float
    ethos: float
    source: str

    def to_dict(self) -> Dict[str, Any]:
        """Converts the signal to a dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Converts the signal to a JSON string."""
        return json.dumps(self.to_dict())
