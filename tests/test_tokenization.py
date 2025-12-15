import unittest
from src.spm_defense.tokenization import HyperToken

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

if __name__ == '__main__':
    unittest.main()
