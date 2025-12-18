import unittest
from spm_defense.tokenization import HyperToken


class TestTokenization(unittest.TestCase):
    def test_hyper_token_initialization(self):
        emb = [0.1, 0.2, 0.3]
        token = HyperToken(embedding=emb)
        self.assertEqual(token.embedding, emb)
        self.assertEqual(token.trajectory, [])
        self.assertEqual(token.mass, 0.0)

    def test_hyper_token_full_init(self):
        emb = [0.1, 0.2, 0.3]
        traj = [[0.0, 0.0, 0.0], [0.1, 0.2, 0.3]]
        mass = 10.5
        token = HyperToken(embedding=emb, trajectory=traj, mass=mass)
        self.assertEqual(token.embedding, emb)
        self.assertEqual(token.trajectory, traj)
        self.assertEqual(token.mass, mass)

    def test_update_trajectory(self):
        # Start at [0, 0]
        token = HyperToken(embedding=[0.0, 0.0])

        # Move to [1, 0]
        token.update_trajectory([1.0, 0.0])

        # Expect trajectory to contain Start and Move: [[0,0], [1,0]]
        self.assertEqual(len(token.trajectory), 2)
        self.assertEqual(token.trajectory[0], [0.0, 0.0])
        self.assertEqual(token.trajectory[1], [1.0, 0.0])
        self.assertEqual(token.embedding, [1.0, 0.0])

        # Move to [1, 1]
        token.update_trajectory([1.0, 1.0])
        self.assertEqual(len(token.trajectory), 3)
        self.assertEqual(token.trajectory[2], [1.0, 1.0])
        self.assertEqual(token.embedding, [1.0, 1.0])

    def test_calculate_stability_no_movement(self):
        token = HyperToken(embedding=[0.0, 0.0])
        # Stability should be max (1000.0) if no trajectory or only 1 point
        self.assertEqual(token.calculate_stability(), 1000.0)

        token.update_trajectory([0.0, 0.0])  # "Move" to same spot
        # Variance is 0. Stability should be max.
        self.assertEqual(token.calculate_stability(), 1000.0)

    def test_calculate_stability_movement(self):
        # Points: (0,0) and (2,0). Centroid (1,0).
        # Dists sq: (1)^2 + (-1)^2 = 1 + 1 = 2.
        # Variance = 2 / 2 = 1.
        # Stability = 1 / (1 + eps) approx 1.0
        token = HyperToken(embedding=[0.0, 0.0])
        token.update_trajectory([2.0, 0.0])

        stab = token.calculate_stability()
        self.assertAlmostEqual(stab, 1.0, places=4)

    def test_estimate_mass(self):
        # Centrality 10. Stability ~1.0 (from prev test)
        token = HyperToken(embedding=[0.0, 0.0])
        token.update_trajectory([2.0, 0.0])

        # Mass = alpha*C + beta*S = 1*10 + 1*1 = 11
        mass = token.estimate_mass(centrality=10.0)
        self.assertAlmostEqual(mass, 11.0, places=4)


if __name__ == '__main__':
    unittest.main()
