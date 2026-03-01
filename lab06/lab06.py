"""
Lab 06: Structured Output with Pydantic and Ollama

This lab demonstrates how to use Pydantic models with Ollama's `format`
parameter to get structured, validated JSON output from an LLM.
"""

from typing import List

import ollama
from pydantic import BaseModel, Field


MODEL = "llama3.2:latest"


# ============================================================================
# Pydantic Models (provided -- do not modify)
# ============================================================================

class AbilityScores(BaseModel):
    strength: int = Field(..., ge=1, le=20, description="Strength score")
    dexterity: int = Field(..., ge=1, le=20, description="Dexterity score")
    constitution: int = Field(..., ge=1, le=20, description="Constitution score")
    intelligence: int = Field(..., ge=1, le=20, description="Intelligence score")
    wisdom: int = Field(..., ge=1, le=20, description="Wisdom score")
    charisma: int = Field(..., ge=1, le=20, description="Charisma score")


class CharacterSheet(BaseModel):
    name: str = Field(..., min_length=1, description="Character name")
    race: str = Field(..., min_length=1, description="Character race, e.g. Elf, Dwarf, Human")
    char_class: str = Field(..., min_length=1, description="Character class, e.g. Wizard, Fighter, Rogue")
    level: int = Field(..., ge=1, le=20, description="Character level")
    ability_scores: AbilityScores
    hit_points: int = Field(..., ge=1, description="Maximum hit points")
    backstory: str = Field(..., min_length=1, description="Brief character backstory")


class MonsterStats(BaseModel):
    name: str = Field(..., min_length=1, description="Monster name")
    monster_type: str = Field(..., min_length=1, description="Monster type, e.g. Undead, Beast, Dragon")
    challenge_rating: float = Field(..., ge=0, le=30, description="Challenge rating")
    hit_points: int = Field(..., ge=1, description="Hit points")
    armor_class: int = Field(..., ge=1, le=30, description="Armor class")
    abilities: List[str] = Field(..., min_length=1, description="List of special abilities")
    description: str = Field(..., min_length=1, description="Physical description of the monster")


class Encounter(BaseModel):
    title: str = Field(..., min_length=1, description="Encounter title")
    setting: str = Field(..., min_length=1, description="Description of where the encounter takes place")
    monsters: List[MonsterStats] = Field(..., min_length=1, description="Monsters in this encounter")
    difficulty: str = Field(..., description="Encounter difficulty: Easy, Medium, Hard, or Deadly")
    treasure: List[str] = Field(default_factory=list, description="Possible treasure rewards")
    narrative_hook: str = Field(..., min_length=1, description="Story hook that leads into this encounter")


# ============================================================================
# Functions to implement
# ============================================================================

def generate_character(description: str) -> CharacterSheet:
    """
    Generate a D&D character sheet from a natural language description.

    Use ollama.chat() with the `format` parameter to get structured output.
    The format parameter should be set to CharacterSheet.model_json_schema().

    Steps:
        1. Call ollama.chat() with:
           - model: MODEL
           - messages: a system message instructing the LLM to create a D&D
             character, and a user message containing the description
           - format: the JSON schema from CharacterSheet
        2. Parse the response with CharacterSheet.model_validate_json()
        3. Return the CharacterSheet instance

    Refer to the Ollama Python API for more information:
    https://github.com/ollama/ollama-python

    Args:
        description: A natural language description of the desired character,
                     e.g. "A wise old elven wizard who studied at the Arcane Academy"

    Returns:
        A validated CharacterSheet instance
    """
    system_msg = {
        "role": "system",
        "content": (
            "You are a Dungeons & Dragons character generator. "
            "Given a short description, produce a JSON object that matches the provided schema exactly. "
            "Do not include any additional text, explanations, or markdown — only the JSON."
        ),
    }

    user_msg = {"role": "user", "content": f"Create a character: {description}"}

    response = ollama.chat(
        model=MODEL,
        messages=[system_msg, user_msg],
        format=CharacterSheet.model_json_schema(),
    )

    # Parse and validate the JSON response into the Pydantic model
    return CharacterSheet.model_validate_json(response.message.content)


def generate_monster(concept: str) -> MonsterStats:
    """
    Generate D&D monster stats from a concept description.

    Use the same structured output pattern as generate_character,
    but with the MonsterStats schema.

    Args:
        concept: A concept for the monster,
                 e.g. "A fire-breathing turtle that lives in volcanic caves"

    Returns:
        A validated MonsterStats instance
    """
    system_msg = {
        "role": "system",
        "content": (
            "You are a Dungeons & Dragons monster generator. "
            "Given a short concept, produce a JSON object that matches the provided schema exactly. "
            "Return only the JSON with no extra commentary."
        ),
    }

    user_msg = {"role": "user", "content": f"Create a monster from this concept: {concept}"}

    response = ollama.chat(
        model=MODEL,
        messages=[system_msg, user_msg],
        format=MonsterStats.model_json_schema(),
    )

    return MonsterStats.model_validate_json(response.message.content)


def generate_encounter(party_level: int, num_monsters: int, theme: str) -> Encounter:
    """
    Generate a complete D&D encounter with nested structured output.

    This function demonstrates nested Pydantic models -- the Encounter model
    contains a list of MonsterStats. The LLM must produce valid JSON for
    the entire nested structure.

    The prompt should instruct the LLM to:
    - Create an encounter appropriate for the given party level
    - Include the requested number of monsters
    - Follow the given theme
    - Set difficulty to exactly one of: Easy, Medium, Hard, or Deadly

    Args:
        party_level: The level of the player party (1-20)
        num_monsters: How many monsters to include in the encounter
        theme: A thematic description, e.g. "undead dungeon", "forest ambush"

    Returns:
        A validated Encounter instance
    """
    system_msg = {
        "role": "system",
        "content": (
            "You are a Dungeons & Dragons encounter designer. "
            "Produce a single JSON object that exactly matches the provided Encounter schema. "
            "The `difficulty` field must be one of: Easy, Medium, Hard, or Deadly. "
            "Include exactly the requested number of monsters in the `monsters` list. "
            "Do not include any text outside of the JSON response."
        ),
    }

    user_msg = {
        "role": "user",
        "content": (
            f"Design an encounter for a party of level {party_level} with {num_monsters} "
            f"monster(s). Theme: {theme}. Make the monsters appropriate for the party level. "
            "Provide a short title, setting, narrative_hook, difficulty (Exact: Easy/Medium/Hard/Deadly), "
            "a list of treasure strings (if any), and a list of monsters matching the MonsterStats schema."
        ),
    }

    response = ollama.chat(
        model=MODEL,
        messages=[system_msg, user_msg],
        format=Encounter.model_json_schema(),
    )

    return Encounter.model_validate_json(response.message.content)


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("=== Generating Character ===")
    character = generate_character("A brave halfling rogue who grew up on the streets")
    print(character.model_dump_json(indent=2))

    print("\n=== Generating Monster ===")
    monster = generate_monster("A shadow wolf that phases through walls")
    print(monster.model_dump_json(indent=2))

    print("\n=== Generating Encounter ===")
    encounter = generate_encounter(party_level=3, num_monsters=2, theme="haunted forest")
    print(encounter.model_dump_json(indent=2))
