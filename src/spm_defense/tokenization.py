from dataclasses import dataclass, field
from typing import List

@dataclass
class HyperToken:
    """
    Represents a Hyper-Token as defined in the SPM v3.0 spec.
    Aggregates tokens to preserve mass and traces trajectory.

    Attributes:
        embedding (List[float]): The standard embedding vector.
        trajectory (List[List[float]]): A history of previous positions/vectors.
        mass (float): The token's calculated Semantic Mass.
    """
    embedding: List[float]
    trajectory: List[List[float]] = field(default_factory=list)
    mass: float = 0.0
