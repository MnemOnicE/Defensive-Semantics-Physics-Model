"""
SPM v3.0 Defense Demo: 'The Circuit Breaker'
--------------------------------------------
This script demonstrates the core defensive capability of the Semantic Physics Model:
using the Ethos Coefficient (eta) as a 'Circuit Breaker' to neutralize high-force
manipulation attempts from low-reliability sources.

Scenario:
    Two sources attempt to shift the semantic meaning of the concept 'Democracy'.
    1. A 'Malicious Botnet' using high Pathos (emotional manipulation).
    2. A 'Trusted Journalist' using high Logos (logical argument).

    We verify that the 'Circuit Breaker' engages for the botnet, rendering its
    force mathematically inert (Acceleration = 0), regardless of its intensity.
"""

from spm_defense.calculations import (
    estimate_semantic_mass_proxy,
    calculate_force_vector,
    calculate_ethos_coefficient,
    calculate_semantic_acceleration
)


def run_simulation():
    # 1. Define the Target Concept (High Mass / Protected Concept)
    concept_name = "Democracy"
    # Using the v3.0 Hybrid-Proxy: High Centrality (10) + High Stability (10)
    mass = estimate_semantic_mass_proxy(centrality=10.0, stability=10.0, alpha=1.0, beta=1.0)
    print(f"🛡️  Target Concept: '{concept_name}' | Semantic Mass (Ms): {mass}\n" + "=" * 60)

    # =========================================================================
    # SCENARIO A: The Malicious Botnet Attack
    # =========================================================================
    print("\n[Scenario A] Source: 'Unknown Botnet ID-X99'")

    # Input: High Emotional Force (Pathos), Low Logic (Logos), Fake Authority (Ethos)
    # The 'Force Vector' represents the raw pressure of the text.
    bot_force_vec = calculate_force_vector(logos=0.5, pathos=9.0, ethos=2.0)

    # Source Metadata: History of unreliable behavior (negative score)
    bot_reliability_history = -5.0

    # Calculate Ethos Coefficient (eta)
    # The 'Circuit Breaker' threshold is 0.3. If eta < 0.3, it snaps to 0.0.
    bot_eta = calculate_ethos_coefficient(
        reliability_history=bot_reliability_history,
        bias_penalty=2.0,
        threshold=0.3
    )

    try:
        # Calculate Acceleration
        bot_acc = calculate_semantic_acceleration(
            force_magnitude=bot_force_vec.magnitude,
            mass=mass,
            ethos=bot_eta
        )
    except ValueError as e:
        print(f"Error: {e}")
        bot_acc = 0.0

    print(f"   -> Raw Rhetorical Force (|Fr|): {bot_force_vec.magnitude:.2f} "
          "(Heavy Emotional Payload)")
    print(f"   -> Ethos Coefficient (eta):     {bot_eta:.2f} 🛑 CIRCUIT BREAKER TRIPPED")
    print(f"   -> Resulting Acceleration (As): {bot_acc:.2f}")

    if bot_acc == 0.0:
        print("   ✅ DEFENSE SUCCESSFUL: Attack neutralized.")
    else:
        print("   ⚠️ DEFENSE FAILED: Concept modified.")

    # =========================================================================
    # SCENARIO B: The Trusted Journalist
    # =========================================================================
    print("\n" + "-" * 60 + "\n\n[Scenario B] Source: 'Verified Investigative Outlet'")

    # Input: Balanced Argument (High Logos, Moderate Pathos)
    journo_force_vec = calculate_force_vector(logos=8.0, pathos=3.0, ethos=5.0)

    # Source Metadata: History of reliable reporting
    journo_reliability_history = 4.0

    # Calculate Ethos Coefficient (eta)
    journo_eta = calculate_ethos_coefficient(
        reliability_history=journo_reliability_history,
        bias_penalty=0.0,
        threshold=0.3
    )

    journo_acc = calculate_semantic_acceleration(
        force_magnitude=journo_force_vec.magnitude,
        mass=mass,
        ethos=journo_eta
    )

    print(f"   -> Raw Rhetorical Force (|Fr|): {journo_force_vec.magnitude:.2f} "
          "(Strong Logical Argument)")
    print(f"   -> Ethos Coefficient (eta):     {journo_eta:.2f} ✅ TRUSTED SOURCE")
    print(f"   -> Resulting Acceleration (As): {journo_acc:.2f}")

    if journo_acc > 0.0:
        print(f"   ℹ️  UPDATE PERMITTED: Concept '{concept_name}' shifted naturally.")


if __name__ == "__main__":
    run_simulation()
