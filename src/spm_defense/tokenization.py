import numpy as np
from dataclasses import dataclass, field
from typing import List
from .calculations import estimate_semantic_mass_proxy


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
        (Spatial Variance).

        Returns:
            float: The stability score. Returns a high value (1000.0)
                   if variance is effectively zero.
        """
        epsilon = 1e-6
        if not self.trajectory:
            return 1.0 / epsilon

        # Convert to numpy array for vector math
        points = np.array(self.trajectory)
        n = len(points)
        if n <= 1:
            return 1.0 / epsilon

        # Calculate Centroid (mean vector)
        centroid = np.mean(points, axis=0)

        # Calculate Spatial Variance: Mean of Squared Euclidean Distances from Centroid
        # (points - centroid) gives vectors from centroid
        # **2 squares each component
        # sum(axis=1) sums squared components to get squared distance
        # mean() averages these squared distances
        squared_distances = np.sum((points - centroid)**2, axis=1)
        variance = np.mean(squared_distances)

        epsilon = 1e-6
        return 1.0 / (variance + epsilon)

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
