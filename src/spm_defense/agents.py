from typing import Dict, List, Optional
from dataclasses import dataclass, field
from .models import SPMSignal
from .tokenization import HyperToken
from .calculations import (
    calculate_force_vector,
    calculate_ethos_coefficient,
    calculate_semantic_acceleration
)


@dataclass
class MonitorAgent:
    """
    A Monitor Agent that tracks semantic acceleration for selected concepts over time.
    It maintains state (HyperTokens) for each concept and processes incoming observations
    to generate SPM Signals.
    """
    concepts: Dict[str, HyperToken] = field(default_factory=dict)
    alpha: float = 1.0  # Mass weighting for centrality
    beta: float = 1.0   # Mass weighting for stability

    # Configuration for alerts (simple thresholding)
    acceleration_threshold: float = 10.0
    ethos_threshold: float = 0.3

    def process_observation(
        self,
        concept: str,
        embedding: List[float],
        logos: float,
        pathos: float,
        ethos_force: float,
        source: str,
        source_reliability: float,
        source_bias: float,
        centrality: float = 1.0
    ) -> SPMSignal:
        """
        Ingests a new observation for a concept and calculates the resulting SPM Signal.

        Args:
            concept (str): The concept being observed.
            embedding (List[float]): The semantic vector of the content.
            logos (float): Rhetorical force component (Logic).
            pathos (float): Rhetorical force component (Emotion).
            ethos_force (float): Rhetorical force component (Source Authority in content).
            source (str): Identifier of the data source.
            source_reliability (float): Historical reliability of the source.
            source_bias (float): Detect bias penalty of the source.
            centrality (float): The network centrality of the concept (default 1.0).

        Returns:
            SPMSignal: The calculated signal containing Mass, Acceleration, etc.
        """
        # 1. Get or Create HyperToken
        if concept not in self.concepts:
            # Initialize with the first embedding
            self.concepts[concept] = HyperToken(embedding=embedding)

        token = self.concepts[concept]

        # 2. Update Trajectory (State Update)
        # Note: If it's a new token, the init set the embedding.
        # If it's existing, we update.
        # We need to handle the first update carefully.
        # If we just created it, the embedding is set.
        # If we call update_trajectory immediately with the same embedding,
        # we might get 0 variance if we aren't careful, but that's physically correct (no movement).
        # However, to simulate 'time', we usually update with the NEW embedding.
        # If the token was just created, we might want to skip update or update with same.
        # For simplicity: Always update. If it's the first point, it adds to trajectory.
        token.update_trajectory(embedding)

        # 3. Calculate Semantic Mass (Ms)
        mass = token.estimate_mass(centrality, self.alpha, self.beta)

        # 4. Calculate Ethos Coefficient (eta) for the SOURCE
        ethos_coeff = calculate_ethos_coefficient(
            source_reliability,
            source_bias,
            threshold=self.ethos_threshold
        )

        # 5. Calculate Rhetorical Force Vector (Fr)
        force_vector = calculate_force_vector(logos, pathos, ethos_force)

        # 6. Calculate Semantic Acceleration (As)
        # |As| = (eta * |Fr|) / Ms
        acceleration = calculate_semantic_acceleration(
            force_vector.magnitude,
            mass,
            ethos_coeff
        )

        # 7. Construct Signal
        signal = SPMSignal(
            concept=concept,
            mass=mass,
            force_vector=force_vector,
            acceleration=acceleration,
            ethos=ethos_coeff,
            source=source
        )

        return signal

    def check_alert(self, signal: SPMSignal) -> Optional[str]:
        """
        Checks if the signal violates safety thresholds.

        Returns:
            Optional[str]: Warning message if triggered, else None.
        """
        warnings = []
        if signal.acceleration > self.acceleration_threshold:
            warnings.append(
                f"High Acceleration ({signal.acceleration:.2f} > {self.acceleration_threshold})"
            )

        # Check for high force from low ethos source (Manipulation attempt)
        if signal.ethos < self.ethos_threshold and signal.force_vector.magnitude > 5.0:
            warnings.append("Low Ethos Source attempting High Force")

        if warnings:
            return f"ALERT [{signal.concept}]: " + "; ".join(warnings)
        return None
