import unittest

from TryReactPy.main import add_one


class TestMain(unittest.TestCase):

    def test_add_one(self):
        self.assertEqual(add_one(5), 6)
