import pytest
from spm_defense.tokenization import HyperToken

def test_hyper_token_initialization():
    emb = [0.1, 0.2, 0.3]
    token = HyperToken(embedding=emb)
    assert token.embedding == emb
    assert token.trajectory == []
    assert token.mass == 0.0

def test_hyper_token_full_init():
    emb = [0.1, 0.2, 0.3]
    traj = [[0.0, 0.0, 0.0], [0.1, 0.2, 0.3]]
    mass = 10.5
    token = HyperToken(embedding=emb, trajectory=traj, mass=mass)
    assert token.embedding == emb
    assert token.trajectory == traj
    assert token.mass == mass

def test_update_trajectory():
    # Start at [0, 0]
    token = HyperToken(embedding=[0.0, 0.0])

    # Move to [1, 0]
    token.update_trajectory([1.0, 0.0])

    # Expect trajectory to contain Start and Move: [[0,0], [1,0]]
    assert len(token.trajectory) == 2
    assert token.trajectory[0] == [0.0, 0.0]
    assert token.trajectory[1] == [1.0, 0.0]
    assert token.embedding == [1.0, 0.0]

    # Move to [1, 1]
    token.update_trajectory([1.0, 1.0])
    assert len(token.trajectory) == 3
    assert token.trajectory[2] == [1.0, 1.0]
    assert token.embedding == [1.0, 1.0]

def test_calculate_stability_no_movement():
    token = HyperToken(embedding=[0.0, 0.0])
    # Stability should be max (1/eps = 1e6) if no trajectory or only 1 point
    assert token.calculate_stability() == 1e6

    token.update_trajectory([0.0, 0.0])  # "Move" to same spot
    # Variance is 0. Stability should be max.
    assert token.calculate_stability() == 1e6

def test_calculate_stability_movement():
    # Points: (0,0) and (2,0). Centroid (1,0).
    # Dists sq: (1)^2 + (-1)^2 = 1 + 1 = 2.
    # Variance = 2 / 2 = 1.
    # Stability = 1 / (1 + eps) approx 1.0
    token = HyperToken(embedding=[0.0, 0.0])
    token.update_trajectory([2.0, 0.0])

    stab = token.calculate_stability()
    assert abs(stab - 1.0) < 1e-4

def test_estimate_mass():
    # Centrality 10. Stability ~1.0 (from prev test)
    token = HyperToken(embedding=[0.0, 0.0])
    token.update_trajectory([2.0, 0.0])

    # Mass = alpha*C + beta*S = 1*10 + 1*1 = 11
    mass = token.estimate_mass(centrality=10.0)
    assert abs(mass - 11.0) < 1e-4
