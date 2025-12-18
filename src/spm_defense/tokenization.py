from dataclasses import dataclass, field
from typing import List
from .calculations import estimate_semantic_mass_proxy


def _euclidean_distance_squared(v1: List[float], v2: List[float]) -> float:
    """Helper to calculate squared euclidean distance between two vectors."""
    return sum((a - b) ** 2 for a, b in zip(v1, v2))


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

    def update_trajectory(self, new_embedding: List[float]) -> None:
        """
        Updates the token's trajectory and moves to the new embedding.

        If the trajectory is empty, the current embedding is added first as the starting point.

        Args:
            new_embedding (List[float]): The new vector position of the token.
        """
        if not self.trajectory:
            self.trajectory.append(self.embedding)

        self.trajectory.append(new_embedding)
        self.embedding = new_embedding

    def calculate_stability(self) -> float:
        """
        Calculates Topological Stability (inverse variance) of the trajectory.

        Formula: T_stability = 1 / (Variance + epsilon)
        Where Variance is the mean squared Euclidean distance from the trajectory's centroid.

        Returns:
            float: The stability score. Returns a high value (1e6) if variance is effectively zero.
        """
        if not self.trajectory:
            # If no history (or just one point which implies 0 variance),
            # stability is theoretically infinite. We clamp it.
            # If we just have the initial embedding but update_trajectory hasn't been called,
            # we effectively have 1 point (current embedding).
            return 1000.0  # High stability constant

        points = self.trajectory
        n = len(points)
        if n <= 1:
            return 1000.0

        dim = len(points[0])
        # Calculate Centroid
        centroid = [sum(pt[i] for pt in points) / n for i in range(dim)]

        # Calculate Variance (Mean Squared Distance from Centroid)
        total_sq_dist = sum(_euclidean_distance_squared(pt, centroid) for pt in points)
        variance = total_sq_dist / n

        epsilon = 1e-6
        if variance < epsilon:
            return 1000.0

        return 1.0 / variance

    def estimate_mass(
        self,
        centrality: float,
        alpha: float = 1.0,
        beta: float = 1.0
    ) -> float:
        """
        Updates and returns the Semantic Mass using the Hybrid-Proxy method.

        Args:
            centrality (float): The graph centrality score.
            alpha (float): Weight for centrality.
            beta (float): Weight for stability.

        Returns:
            float: The calculated mass.
        """
        stability = self.calculate_stability()
        self.mass = estimate_semantic_mass_proxy(centrality, stability, alpha, beta)
        return self.mass
