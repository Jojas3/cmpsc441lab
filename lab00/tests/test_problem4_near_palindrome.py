import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

import pytest
from src.problem4_near_palindrome import is_near_palindrome

@pytest.mark.parametrize(
    "s, expected",
    [
        ("", True),
        ("a", True),
        ("aa", True),
        ("ab", True),
        ("aba", True),
        ("abca", True),
        ("abc", False),
        ("deeee", True),
        ("raceacar", True),
        ("abcdefedcbaa", True),
        ("abecbea", False),
    ],
)
def test_is_near_palindrome(s, expected):
    assert is_near_palindrome(s) == expected
