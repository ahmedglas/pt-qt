import unittest
from context import verificateur


class TestExempleSomme(unittest.TestCase):
    def test_undeux(self):
        somme = verificateur.exemple(1, 2)
        self.assertEqual(somme, 3)
