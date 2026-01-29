"""Tests for dict_json_exercise.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

import json
import pytest

from dict_json_exercise import (
    game_data,
    get_player_intelligence,
    get_health_potion_count,
    get_active_quest_titles,
    calculate_total_weapon_damage,
    add_potion,
    complete_quest_and_get_reward,
    to_pretty_json,
)


@pytest.fixture
def fresh_game_data():
    """Return a fresh copy of game_data for each test."""
    return json.loads(json.dumps(game_data))


def test_get_player_intelligence(fresh_game_data):
    """Exercise 1: Get the player's intelligence stat."""
    result = get_player_intelligence(fresh_game_data)
    assert result == 25


def test_get_health_potion_count(fresh_game_data):
    """Exercise 2: Get the quantity of health potions."""
    result = get_health_potion_count(fresh_game_data)
    assert result == 3


def test_get_active_quest_titles(fresh_game_data):
    """Exercise 3: Get a list of all active quest titles."""
    result = get_active_quest_titles(fresh_game_data)
    assert result == ["Defeat the Dragon", "Find the Lost Tome"]


def test_calculate_total_weapon_damage(fresh_game_data):
    """Exercise 4: Calculate total damage from all weapons."""
    result = calculate_total_weapon_damage(fresh_game_data)
    assert result == 65


def test_add_potion(fresh_game_data):
    """Exercise 5: Add a new potion to the inventory."""
    new_potion = {
        "name": "Stamina Elixir",
        "effect": "boost_stamina",
        "amount": 30,
        "quantity": 2,
    }
    add_potion(fresh_game_data, new_potion)
    
    potions = fresh_game_data["inventory"]["potions"]
    assert len(potions) == 3
    assert potions[-1] == new_potion


def test_complete_quest_and_get_reward(fresh_game_data):
    """Exercise 6: Complete quest and add reward to gold."""
    result = complete_quest_and_get_reward(fresh_game_data, 101)
    assert result == 1750  # 1250 + 500 reward


def test_to_pretty_json():
    """Exercise 7: Convert dictionary to pretty JSON with 4-space indent."""
    result = to_pretty_json({"a": 1})
    expected = '{\n    "a": 1\n}'
    assert result == expected


def test_to_pretty_json_nested():
    """Exercise 7 bonus: Test with nested structure."""
    data = {"player": {"name": "Test", "level": 1}}
    result = to_pretty_json(data)
    assert '"player"' in result
    assert '"name"' in result
    assert '    ' in result  # Should have 4-space indentation
