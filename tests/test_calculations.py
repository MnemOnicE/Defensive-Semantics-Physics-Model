import pytest
import json
import math
from spm_defense.models import SPMSignal, RhetoricalForceVector
from spm_defense.calculations import (
    estimate_semantic_mass_proxy,
    calculate_force_vector,
    calculate_ethos_coefficient,
    calculate_semantic_acceleration
)


def test_spm_signal_serialization():
    force_vec = RhetoricalForceVector(logos=0.8, pathos=0.4, ethos=0.2)
    signal = SPMSignal(
        concept="Democracy",
        mass=50.0,
        force_vector=force_vec,
        acceleration=0.85,
        ethos=0.2,
        source="unknown_botnet"
    )

    json_str = signal.to_json()
    data = json.loads(json_str)

    assert data["concept"] == "Democracy"
    assert data["mass"] == 50.0
    assert data["force_vector"]["logos"] == 0.8
    assert data["force_vector"]["pathos"] == 0.4
    assert data["force_vector"]["ethos"] == 0.2
    assert data["acceleration"] == 0.85
    assert data["ethos"] == 0.2
    assert data["source"] == "unknown_botnet"


def test_estimate_semantic_mass_proxy():
    # Ms = 1.0 * 10 + 1.0 * 5 = 15
    mass = estimate_semantic_mass_proxy(centrality=10, stability=5)
    assert mass == 15

    # Ms = 0.5 * 10 + 2.0 * 5 = 5 + 10 = 15
    mass = estimate_semantic_mass_proxy(
        centrality=10, stability=5, alpha=0.5, beta=2.0
    )
    assert mass == 15


def test_calculate_force_vector():
    # Vector(3, 4, 0) -> Magnitude 5
    vec = calculate_force_vector(logos=3.0, pathos=4.0, ethos=0.0)
    assert vec.logos == 3.0
    assert vec.pathos == 4.0
    assert vec.ethos == 0.0
    assert vec.magnitude == 5.0


def test_ethos_coefficient_logic():
    # eta = sigmoid(0 - 0) = 0.5. Threshold default 0.3. 0.5 > 0.3 -> keep 0.5
    ethos = calculate_ethos_coefficient(reliability_history=0, bias_penalty=0)
    assert ethos == 0.5

    # eta = sigmoid(10 - 0) -> close to 1
    ethos_high = calculate_ethos_coefficient(reliability_history=10, bias_penalty=0)
    assert ethos_high > 0.99


def test_ethos_circuit_breaker():
    # eta = sigmoid(-2) approx 0.119
    # 0.119 < 0.3 -> Should snap to 0.0
    ethos_snap = calculate_ethos_coefficient(
        reliability_history=-2, bias_penalty=0, threshold=0.3
    )
    assert ethos_snap == 0.0

    # Test just above threshold
    # sigmoid(-0.8) approx 0.31 -> should return ~0.31
    ethos_border = calculate_ethos_coefficient(
        reliability_history=-0.8, bias_penalty=0, threshold=0.3
    )
    assert ethos_border > 0.3
    assert math.isclose(ethos_border, 1 / (1 + math.exp(0.8)), rel_tol=1e-5)


def test_ethos_coefficient_boundary():
    # Test EXACT threshold case (edge case)
    # If sigmoid(x) == threshold, does it snap or stay?
    # Implementation: if eta < threshold: return 0.0. So equal should stay.

    # Let's verify behavior with a contrived threshold.
    # eta = 0.5. threshold = 0.5.
    ethos = calculate_ethos_coefficient(reliability_history=0, bias_penalty=0, threshold=0.5)
    assert ethos == 0.5

    # eta = 0.5. threshold = 0.5000001
    ethos_snap = calculate_ethos_coefficient(
        reliability_history=0, bias_penalty=0, threshold=0.5000001
    )
    assert ethos_snap == 0.0


def test_semantic_acceleration():
    # As = (0.5 * 10) / 5 = 1.0
    acc = calculate_semantic_acceleration(
        force_magnitude=10, mass=5, ethos=0.5
    )
    assert acc == 1.0

    # Integration test style
    vec = calculate_force_vector(3, 4, 0)  # mag 5
    acc_integ = calculate_semantic_acceleration(
        force_magnitude=vec.magnitude, mass=5, ethos=1.0
    )
    assert acc_integ == 1.0


def test_semantic_acceleration_zero_mass():
    with pytest.raises(ValueError, match="Semantic Mass cannot be zero"):
        calculate_semantic_acceleration(force_magnitude=10, mass=0, ethos=0.5)

    # Test approaching zero (very small mass)
    # Should result in huge acceleration, but not fail
    acc_huge = calculate_semantic_acceleration(force_magnitude=10, mass=1e-9, ethos=0.5)
    assert acc_huge == 5e9
