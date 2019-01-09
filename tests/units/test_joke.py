import pytest
from app.app import get_joke


def test_joke():
    joke = get_joke()
    assert isinstance(joke, str) == True