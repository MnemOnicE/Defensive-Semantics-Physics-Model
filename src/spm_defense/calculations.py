import math
from .models import RhetoricalForceVector


def sigmoid(x: float) -> float:
    """Standard sigmoid function."""
    return 1 / (1 + math.exp(-x))


def estimate_semantic_mass_proxy(
    centrality: float,
    stability: float,
    alpha: float = 1.0,
    beta: float = 1.0
) -> float:
    """
    Calculates Semantic Mass (Ms) for a concept.
    Approximates the v3.0 Topological Stability (Ms) using efficient graph centrality
    and variance proxies, as defined in the Hybrid-Proxy Protocol.

    Formula: Ms(c) = alpha * C(c) + beta * T_stability(c)

    Args:
        centrality (float): Network centrality score (C).
        stability (float): Historical stability/inverse variance (T_stability).
        alpha (float): Weighting constant for centrality. Default is 1.0.
        beta (float): Weighting constant for stability. Default is 1.0.

    Returns:
        float: The calculated Semantic Mass.
    """
    return alpha * centrality + beta * stability


def calculate_force_vector(
    logos: float,
    pathos: float,
    ethos: float
) -> RhetoricalForceVector:
    """
    Calculates the Rhetorical Force Vector (Fr).

    Args:
        logos (float): Logic/Evidence force score.
        pathos (float): Emotional force score.
        ethos (float): Source authority force score.

    Returns:
        RhetoricalForceVector: The decomposed rhetorical force vector.
    """
    return RhetoricalForceVector(logos=logos, pathos=pathos, ethos=ethos)


def calculate_ethos_coefficient(
    reliability_history: float,
    bias_penalty: float,
    threshold: float = 0.3
) -> float:
    """
    Calculates the Ethos Coefficient (eta).

    Formula: eta(s) = sigmoid(R_history(s) - P_bias(s))

    If the calculated eta is less than the threshold, it snaps to 0.0 (Circuit Breaker).

    Args:
        reliability_history (float): Historical reliability score (R_history).
        bias_penalty (float): Detected bias penalty (P_bias).
        threshold (float): The Circuit Breaker threshold. Default is 0.3.

    Returns:
        float: The Ethos Coefficient, normalized between 0 and 1.
    """
    eta = sigmoid(reliability_history - bias_penalty)
    if eta < threshold:
        return 0.0
    return eta


def calculate_semantic_acceleration(
    force_magnitude: float,
    mass: float,
    ethos: float
) -> float:
    """
    Calculates the magnitude of Semantic Acceleration (As).

    Formula: |As| = (eta * |Fr|) / Ms

    Args:
        force_magnitude (float): The magnitude of Rhetorical Force (|Fr|).
        mass (float): The Semantic Mass (Ms).
        ethos (float): The Ethos Coefficient (eta).

    Returns:
        float: The magnitude of Semantic Acceleration.

    Raises:
        ValueError: If mass is 0.
    """
    if mass == 0:
        raise ValueError("Semantic Mass cannot be zero.")

    return (ethos * force_magnitude) / mass
