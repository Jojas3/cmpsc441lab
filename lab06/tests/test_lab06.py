import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import pytest
from lab06.lab06 import (
    generate_character,
    generate_monster,
    generate_encounter,
    CharacterSheet,
    MonsterStats,
    Encounter,
    AbilityScores,
)


@pytest.mark.parametrize("description", [
    "A wise old elven wizard who studied at the Arcane Academy",
    "A fierce dwarven barbarian from the northern mountains",
    "A cunning human rogue who works as a spy",
])
def test_generate_character(description):
    result = generate_character(description)

    assert isinstance(result, CharacterSheet)

    # Non-empty strings
    assert len(result.name) > 0
    assert len(result.race) > 0
    assert len(result.char_class) > 0
    assert len(result.backstory) > 0

    # Ability scores within range
    assert isinstance(result.ability_scores, AbilityScores)
    for attr in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
        score = getattr(result.ability_scores, attr)
        assert 1 <= score <= 20, f"{attr} = {score} is out of range"

    # Level and HP
    assert 1 <= result.level <= 20
    assert result.hit_points >= 1


@pytest.mark.parametrize("concept", [
    "A fire-breathing turtle that lives in volcanic caves",
    "An ancient ghost that haunts a ruined library",
])
def test_generate_monster(concept):
    result = generate_monster(concept)

    assert isinstance(result, MonsterStats)

    assert len(result.name) > 0
    assert len(result.monster_type) > 0
    assert len(result.description) > 0
    assert 0 <= result.challenge_rating <= 30
    assert result.hit_points >= 1
    assert 1 <= result.armor_class <= 30
    assert len(result.abilities) >= 1
    assert all(isinstance(a, str) and len(a) > 0 for a in result.abilities)


@pytest.mark.parametrize("party_level,num_monsters,theme", [
    (3, 2, "haunted forest"),
    (7, 3, "dragon's lair"),
])
def test_generate_encounter(party_level, num_monsters, theme):
    result = generate_encounter(party_level, num_monsters, theme)

    assert isinstance(result, Encounter)

    assert len(result.title) > 0
    assert len(result.setting) > 0
    assert len(result.narrative_hook) > 0
    assert result.difficulty in ["Easy", "Medium", "Hard", "Deadly"]

    # Monsters are valid MonsterStats
    assert len(result.monsters) >= 1
    for monster in result.monsters:
        assert isinstance(monster, MonsterStats)
        assert len(monster.name) > 0
        assert monster.hit_points >= 1
