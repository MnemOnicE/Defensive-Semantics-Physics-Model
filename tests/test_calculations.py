import unittest
import json
import math
from spm_defense.models import SPMSignal, RhetoricalForceVector
from spm_defense.calculations import (
    estimate_semantic_mass_proxy,
    calculate_force_vector,
    calculate_ethos_coefficient,
    calculate_semantic_acceleration
)


class TestSPMModels(unittest.TestCase):
    def test_spm_signal_serialization(self):
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

        self.assertEqual(data["concept"], "Democracy")
        self.assertEqual(data["mass"], 50.0)
        # Check nested dictionary for force_vector
        self.assertEqual(data["force_vector"]["logos"], 0.8)
        self.assertEqual(data["force_vector"]["pathos"], 0.4)
        self.assertEqual(data["force_vector"]["ethos"], 0.2)
        self.assertEqual(data["acceleration"], 0.85)
        self.assertEqual(data["ethos"], 0.2)
        self.assertEqual(data["source"], "unknown_botnet")


class TestSPMCalculations(unittest.TestCase):

    def test_estimate_semantic_mass_proxy(self):
        # Ms = 1.0 * 10 + 1.0 * 5 = 15
        mass = estimate_semantic_mass_proxy(centrality=10, stability=5)
        self.assertEqual(mass, 15)

        # Ms = 0.5 * 10 + 2.0 * 5 = 5 + 10 = 15
        mass = estimate_semantic_mass_proxy(
            centrality=10, stability=5, alpha=0.5, beta=2.0
        )
        self.assertEqual(mass, 15)

    def test_calculate_force_vector(self):
        # Test vector creation and magnitude
        # Vector(3, 4, 0) -> Magnitude 5
        vec = calculate_force_vector(logos=3.0, pathos=4.0, ethos=0.0)
        self.assertEqual(vec.logos, 3.0)
        self.assertEqual(vec.pathos, 4.0)
        self.assertEqual(vec.ethos, 0.0)
        self.assertEqual(vec.magnitude, 5.0)

    def test_ethos_coefficient(self):
        # eta = sigmoid(0 - 0) = 0.5. Threshold default 0.3. 0.5 > 0.3 -> keep 0.5
        ethos = calculate_ethos_coefficient(reliability_history=0, bias_penalty=0)
        self.assertEqual(ethos, 0.5)

        # eta = sigmoid(10 - 0) -> close to 1
        ethos_high = calculate_ethos_coefficient(reliability_history=10, bias_penalty=0)
        self.assertGreater(ethos_high, 0.99)

        # Circuit Breaker Test
        # eta = sigmoid(-2) approx 0.119
        # 0.119 < 0.3 -> Should snap to 0.0
        ethos_snap = calculate_ethos_coefficient(
            reliability_history=-2, bias_penalty=0, threshold=0.3
        )
        self.assertEqual(ethos_snap, 0.0)

        # Test just above threshold
        # We need sigmoid(x) > 0.3
        # sigmoid(-0.8) approx 0.31 -> should return ~0.31
        ethos_border = calculate_ethos_coefficient(
            reliability_history=-0.8, bias_penalty=0, threshold=0.3
        )
        self.assertGreater(ethos_border, 0.3)
        self.assertAlmostEqual(ethos_border, 1 / (1 + math.exp(0.8)))

    def test_semantic_acceleration(self):
        # As = (0.5 * 10) / 5 = 1.0
        acc = calculate_semantic_acceleration(
            force_magnitude=10, mass=5, ethos=0.5
        )
        self.assertEqual(acc, 1.0)

        # Integration test style
        vec = calculate_force_vector(3, 4, 0)  # mag 5
        acc_integ = calculate_semantic_acceleration(
            force_magnitude=vec.magnitude, mass=5, ethos=1.0
        )
        self.assertEqual(acc_integ, 1.0)

    def test_semantic_acceleration_zero_mass(self):
        with self.assertRaises(ValueError):
            calculate_semantic_acceleration(force_magnitude=10, mass=0, ethos=0.5)


if __name__ == '__main__':
    unittest.main()
