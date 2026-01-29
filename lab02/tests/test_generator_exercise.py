"""Tests for generator_exercise.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

import pytest

from generator_exercise import (
    infinite_counter,
    color_cycle,
    take_n,
)


class TestInfiniteCounter:
    """Exercise 1: Infinite counter generator using next()."""

    def test_counter_starts_at_zero(self):
        counter = infinite_counter(0)
        assert next(counter) == 0
        assert next(counter) == 1
        assert next(counter) == 2

    def test_counter_starts_at_custom_value(self):
        counter = infinite_counter(10)
        assert next(counter) == 10
        assert next(counter) == 11
        assert next(counter) == 12

    def test_counter_negative_start(self):
        counter = infinite_counter(-2)
        assert next(counter) == -2
        assert next(counter) == -1
        assert next(counter) == 0
        assert next(counter) == 1

    def test_counter_many_calls(self):
        counter = infinite_counter(0)
        for i in range(100):
            assert next(counter) == i


class TestColorCycle:
    """Exercise 2: Cycling generator using next()."""

    def test_cycle_three_colors(self):
        colors = color_cycle(["red", "green", "blue"])
        assert next(colors) == "red"
        assert next(colors) == "green"
        assert next(colors) == "blue"
        assert next(colors) == "red"  # wraps around
        assert next(colors) == "green"

    def test_cycle_two_items(self):
        toggle = color_cycle(["on", "off"])
        assert next(toggle) == "on"
        assert next(toggle) == "off"
        assert next(toggle) == "on"
        assert next(toggle) == "off"

    def test_cycle_single_item(self):
        single = color_cycle(["only"])
        assert next(single) == "only"
        assert next(single) == "only"
        assert next(single) == "only"

    def test_cycle_numbers(self):
        nums = color_cycle([1, 2, 3])
        results = [next(nums) for _ in range(7)]
        assert results == [1, 2, 3, 1, 2, 3, 1]


class TestTakeN:
    """Exercise 3: Extract n values from a generator."""

    def test_take_from_infinite_counter(self):
        counter = infinite_counter(0)
        result = take_n(counter, 5)
        assert result == [0, 1, 2, 3, 4]

    def test_take_continues_from_where_left_off(self):
        counter = infinite_counter(0)
        first_batch = take_n(counter, 5)
        second_batch = take_n(counter, 3)
        assert first_batch == [0, 1, 2, 3, 4]
        assert second_batch == [5, 6, 7]

    def test_take_from_color_cycle(self):
        colors = color_cycle(["A", "B"])
        result = take_n(colors, 5)
        assert result == ["A", "B", "A", "B", "A"]

    def test_take_zero(self):
        counter = infinite_counter(0)
        result = take_n(counter, 0)
        assert result == []

    def test_take_one(self):
        counter = infinite_counter(42)
        result = take_n(counter, 1)
        assert result == [42]
