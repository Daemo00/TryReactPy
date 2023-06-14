import unittest

from TryReactPy.main import app


class TestMain(unittest.TestCase):

    def test_app(self):
        self.assertIn("Hello", app().render()['children'][0])
