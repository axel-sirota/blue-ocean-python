import unittest
import app


class TestJoke(unittest.TestCase):

    def test_joke(self):
        joke = app.get_joke()
        self.assertEqual(isinstance(joke, str), True)
