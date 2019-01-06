import unittest
from app.app import get_joke


class TestJoke(unittest.TestCase):

    def test_joke(self):
        joke = get_joke()
        self.assertEqual(isinstance(joke, str), True)
