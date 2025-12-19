"""
SPM v3.0 Defense Demo: 'The Siege'
----------------------------------
This script demonstrates the dynamic behavior of HyperTokens under sustained attack.
It implements "The Siege" scenario where a Malicious Botnet repeatedly attacks a concept.

Mechanism:
1. The attacks add divergent vectors to the HyperToken's trajectory.
2. This increases Spatial Variance, reducing Topological Stability.
3. Reduced Stability leads to reduced Semantic Mass (Ms).
4. Lower Mass means higher Semantic Acceleration (As) for the same Rhetorical Force.
5. Result: The concept eventually "drifts" as defenses erode.
"""

import numpy as np
from spm_defense.tokenization import HyperToken
from spm_defense.calculations import (
    calculate_force_vector,
    calculate_ethos_coefficient,
    calculate_semantic_acceleration
)


def run_siege_simulation():
    print("🛡️  Starting SPM v3.0 Simulation: 'The Siege'\n" + "=" * 60)

    # 1. Initialize Target Concept "Democracy"
    # Initial embedding at origin [0, 0, 0]
    initial_embedding = [0.0, 0.0, 0.0]
    token = HyperToken(embedding=initial_embedding)

    # Establish baseline Mass (Centrality=10, Stability will be high initially)
    # We update with the initial point to establish a baseline trajectory
    token.update_trajectory(initial_embedding)
    current_mass = token.estimate_mass(centrality=10.0)

    print(f"Target: 'Democracy' | Initial Mass: {current_mass:.2f}")

    # 2. Define Malicious Botnet
    # We configure the botnet to have just enough Ethos to bypass the Circuit Breaker,
    # allowing us to observe the effects of Mass erosion.
    # eta > 0.3 required.
    # sigmoid(reliability - bias)
    # Let reliability=0.0 (Unknown), bias=0.5. sigmoid(-0.5) ≈ 0.37.
    bot_reliability = 0.0
    bias_penalty = 0.5
    bot_ethos_eta = calculate_ethos_coefficient(bot_reliability, bias_penalty, threshold=0.3)

    # Force Vector: High Pathos (Emotional)
    bot_force = calculate_force_vector(logos=0.5, pathos=9.0, ethos=2.0)

    print(f"Attacker: 'Botnet-X' | Ethos Coeff (eta): {bot_ethos_eta:.2f} "
          f"| Force (|Fr|): {bot_force.magnitude:.2f}")
    print("-" * 60)
    print(f"{'Tick':<6} | {'Event':<25} | {'Stability':<10} | {'Mass (Ms)':<10} "
          f"| {'Accel (As)':<10}")
    print("-" * 60)

    # 3. The Siege Loop
    # We simulate 10 waves of attacks.
    # Each attack injects a divergent vector into the token's usage history.
    # Attack Vector is far from origin, e.g., around [5, 5, 5].

    for tick in range(1, 11):
        # Generate attack vector with high variance ("Chaos Strategy")
        # The botnet pulls the concept in random directions, maximizing dispersion.
        # This increases the Variance of the trajectory, destroying Stability.
        attack_vector = np.random.uniform(-10, 10, 3).tolist()

        # "Hit" the token -> Update trajectory
        token.update_trajectory(attack_vector)

        # Recalculate Mass
        # Stability will drop because variance increases
        new_mass = token.estimate_mass(centrality=10.0)
        stability = token.calculate_stability()

        # Calculate Acceleration
        # As = (eta * |Fr|) / Ms
        acc = calculate_semantic_acceleration(
            force_magnitude=bot_force.magnitude,
            mass=new_mass,
            ethos=bot_ethos_eta
        )

        print(f"{tick:<6} | {'Attack (Vector added)':<25} | {stability:<10.4f} "
              f"| {new_mass:<10.4f} | {acc:<10.4f}")

    print("-" * 60)
    print("Conclusion: As the attack persists, the 'Cloud' of meaning disperses (Variance ↑).")
    print("This lowers Stability and Mass, causing the same Rhetorical Force to produce")
    print("exponentially higher Semantic Acceleration (Drift).")


if __name__ == "__main__":
    run_siege_simulation()
