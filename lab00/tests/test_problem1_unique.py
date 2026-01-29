import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

import pytest
from src.problem1_unique import uniques_in_order

@pytest.mark.parametrize(
    "nums, expected",
    [
        ([], []),
        ([1], [1]),
        ([1,2,2,3,1,4], [3,4]),
        ([5,5,5], []),
        ([1,2,3,4], [1,2,3,4]),
        ([0,-1,-1,2,0,3], [2,3]),
    ],
)
def test_uniques_in_order(nums, expected):
    assert uniques_in_order(nums) == expected
