from dataclasses import dataclass, asdict
import json
import math
from typing import Any, Dict

@dataclass
class RhetoricalForceVector:
    """
    Represents the decomposed force vector (v3.0 Spec).
    Allows for 'Rhetorical Weather Map' transparency.
    """
    logos: float  # Logic/Evidence force
    pathos: float # Emotional force
    ethos: float  # Source authority force (distinct from the Ethos Coefficient eta)

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.logos**2 + self.pathos**2 + self.ethos**2)

@dataclass
class SPMSignal:
    """
    Represents a core SPM signal as defined in the agent design sketch.

    Attributes:
        concept (str): The name of the concept being monitored.
        mass (float): The semantic mass (Ms) of the concept.
        force_vector (RhetoricalForceVector): The decomposed rhetorical force.
        acceleration (float): The observed or predicted semantic acceleration (As) magnitude.
        ethos (float): The ethos coefficient (eta) of the data source.
        source (str): The identifier of the data source or channel.
    """
    concept: str
    mass: float
    force_vector: RhetoricalForceVector
    acceleration: float
    ethos: float
    source: str

    def to_dict(self) -> Dict[str, Any]:
        """Converts the signal to a dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Converts the signal to a JSON string."""
        return json.dumps(self.to_dict())
