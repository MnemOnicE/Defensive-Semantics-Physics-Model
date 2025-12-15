import math

def sigmoid(x: float) -> float:
    """Standard sigmoid function."""
    return 1 / (1 + math.exp(-x))

def calculate_semantic_mass(
    centrality: float,
    stability: float,
    alpha: float = 1.0,
    beta: float = 1.0
) -> float:
    """
    Calculates Semantic Mass (Ms) for a concept.

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

def calculate_rhetorical_force_magnitude(
    embedding_magnitude: float,
    sentiment_intensity: float,
    repetition_frequency: float
) -> float:
    """
    Calculates the magnitude of Rhetorical Force (Fr).

    Formula: |Fr| = |V(I)| * (1 + lambda_emotional) * (1 + lambda_repetition)

    Args:
        embedding_magnitude (float): The magnitude of the raw embedding vector |V(I)|.
        sentiment_intensity (float): Sentiment intensity score (lambda_emotional).
        repetition_frequency (float): Frequency of the concept in input (lambda_repetition).

    Returns:
        float: The magnitude of Rhetorical Force.
    """
    return embedding_magnitude * (1 + sentiment_intensity) * (1 + repetition_frequency)

def calculate_ethos_coefficient(
    reliability_history: float,
    bias_penalty: float
) -> float:
    """
    Calculates the Ethos Coefficient (eta).

    Formula: eta(s) = sigmoid(R_history(s) - P_bias(s))

    Args:
        reliability_history (float): Historical reliability score (R_history).
        bias_penalty (float): Detected bias penalty (P_bias).

    Returns:
        float: The Ethos Coefficient, normalized between 0 and 1.
    """
    return sigmoid(reliability_history - bias_penalty)

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
