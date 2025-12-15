import unittest
import json
from src.spm_defense.models import SPMSignal
from src.spm_defense.calculations import (
    calculate_semantic_mass,
    calculate_rhetorical_force_magnitude,
    calculate_ethos_coefficient,
    calculate_semantic_acceleration,
    sigmoid
)

class TestSPMModels(unittest.TestCase):
    def test_spm_signal_serialization(self):
        signal = SPMSignal(
            concept="Democracy",
            mass=50.0,
            acceleration=0.85,
            ethos=0.2,
            source="unknown_botnet"
        )

        json_str = signal.to_json()
        data = json.loads(json_str)

        self.assertEqual(data["concept"], "Democracy")
        self.assertEqual(data["mass"], 50.0)
        self.assertEqual(data["acceleration"], 0.85)
        self.assertEqual(data["ethos"], 0.2)
        self.assertEqual(data["source"], "unknown_botnet")

class TestSPMCalculations(unittest.TestCase):

    def test_semantic_mass(self):
        # Ms = 1.0 * 10 + 1.0 * 5 = 15
        mass = calculate_semantic_mass(centrality=10, stability=5)
        self.assertEqual(mass, 15)

        # Ms = 0.5 * 10 + 2.0 * 5 = 5 + 10 = 15
        mass = calculate_semantic_mass(centrality=10, stability=5, alpha=0.5, beta=2.0)
        self.assertEqual(mass, 15)

    def test_rhetorical_force_magnitude(self):
        # |Fr| = 2.0 * (1 + 0.5) * (1 + 0.1) = 2.0 * 1.5 * 1.1 = 3.3
        force = calculate_rhetorical_force_magnitude(
            embedding_magnitude=2.0,
            sentiment_intensity=0.5,
            repetition_frequency=0.1
        )
        self.assertAlmostEqual(force, 3.3)

    def test_ethos_coefficient(self):
        # eta = sigmoid(0 - 0) = 0.5
        ethos = calculate_ethos_coefficient(reliability_history=0, bias_penalty=0)
        self.assertEqual(ethos, 0.5)

        # eta = sigmoid(10 - 0) -> close to 1
        ethos_high = calculate_ethos_coefficient(reliability_history=10, bias_penalty=0)
        self.assertGreater(ethos_high, 0.99)

        # eta = sigmoid(0 - 10) -> close to 0
        ethos_low = calculate_ethos_coefficient(reliability_history=0, bias_penalty=10)
        self.assertLess(ethos_low, 0.01)

    def test_semantic_acceleration(self):
        # As = (0.5 * 10) / 5 = 1.0
        acc = calculate_semantic_acceleration(force_magnitude=10, mass=5, ethos=0.5)
        self.assertEqual(acc, 1.0)

    def test_semantic_acceleration_zero_mass(self):
        with self.assertRaises(ValueError):
            calculate_semantic_acceleration(force_magnitude=10, mass=0, ethos=0.5)

if __name__ == '__main__':
    unittest.main()
