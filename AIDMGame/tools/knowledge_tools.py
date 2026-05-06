"""
Knowledge lookup tools for D&D spells, monsters, and rules
"""
from typing import Dict, Any, List


# Spell database
SPELLS = {
    "fireball": {
        "name": "Fireball",
        "level": 3,
        "school": "Evocation",
        "casting_time": "1 action",
        "range": "150 feet",
        "components": "V, S, M (a tiny ball of bat guano and sulfur)",
        "duration": "Instantaneous",
        "description": "A bright streak flashes from your pointing finger to a point you choose within range and then blossoms with a low roar into an explosion of flame. Each creature in a 20-foot-radius sphere centered on that point must make a Dexterity saving throw. A target takes 8d6 fire damage on a failed save, or half as much damage on a successful one.",
        "damage": "8d6",
        "save": "Dexterity"
    },
    "magic missile": {
        "name": "Magic Missile",
        "level": 1,
        "school": "Evocation",
        "casting_time": "1 action",
        "range": "120 feet",
        "components": "V, S",
        "duration": "Instantaneous",
        "description": "You create three glowing darts of magical force. Each dart hits a creature of your choice that you can see within range. A dart deals 1d4 + 1 force damage to its target. The darts all strike simultaneously.",
        "damage": "1d4+1 per dart (3 darts)",
        "save": "None (auto-hit)"
    },
    "cure wounds": {
        "name": "Cure Wounds",
        "level": 1,
        "school": "Evocation",
        "casting_time": "1 action",
        "range": "Touch",
        "components": "V, S",
        "duration": "Instantaneous",
        "description": "A creature you touch regains a number of hit points equal to 1d8 + your spellcasting ability modifier.",
        "healing": "1d8 + modifier",
        "save": "None"
    },
    "shield": {
        "name": "Shield",
        "level": 1,
        "school": "Abjuration",
        "casting_time": "1 reaction",
        "range": "Self",
        "components": "V, S",
        "duration": "1 round",
        "description": "An invisible barrier of magical force appears and protects you. Until the start of your next turn, you have a +5 bonus to AC, including against the triggering attack.",
        "effect": "+5 AC",
        "save": "None"
    },
    "lightning bolt": {
        "name": "Lightning Bolt",
        "level": 3,
        "school": "Evocation",
        "casting_time": "1 action",
        "range": "Self (100-foot line)",
        "components": "V, S, M (a bit of fur and a rod of amber, crystal, or glass)",
        "duration": "Instantaneous",
        "description": "A stroke of lightning forming a line 100 feet long and 5 feet wide blasts out from you in a direction you choose. Each creature in the line must make a Dexterity saving throw. A creature takes 8d6 lightning damage on a failed save, or half as much damage on a successful one.",
        "damage": "8d6",
        "save": "Dexterity"
    }
}


# Monster database
MONSTERS = {
    "goblin": {
        "name": "Goblin",
        "type": "Small humanoid",
        "armor_class": 15,
        "hit_points": 7,
        "speed": "30 ft",
        "str": 8, "dex": 14, "con": 10, "int": 10, "wis": 8, "cha": 8,
        "skills": "Stealth +6",
        "challenge_rating": "1/4",
        "attacks": [
            {"name": "Scimitar", "bonus": 4, "damage": "1d6+2", "type": "slashing"},
            {"name": "Shortbow", "bonus": 4, "damage": "1d6+2", "type": "piercing", "range": "80/320 ft"}
        ],
        "special": "Nimble Escape: The goblin can take the Disengage or Hide action as a bonus action on each of its turns."
    },
    "orc": {
        "name": "Orc",
        "type": "Medium humanoid",
        "armor_class": 13,
        "hit_points": 15,
        "speed": "30 ft",
        "str": 16, "dex": 12, "con": 16, "int": 7, "wis": 11, "cha": 10,
        "skills": "Intimidation +2",
        "challenge_rating": "1/2",
        "attacks": [
            {"name": "Greataxe", "bonus": 5, "damage": "1d12+3", "type": "slashing"},
            {"name": "Javelin", "bonus": 5, "damage": "1d6+3", "type": "piercing", "range": "30/120 ft"}
        ],
        "special": "Aggressive: As a bonus action, the orc can move up to its speed toward a hostile creature that it can see."
    },
    "dragon": {
        "name": "Young Red Dragon",
        "type": "Large dragon",
        "armor_class": 18,
        "hit_points": 178,
        "speed": "40 ft, climb 40 ft, fly 80 ft",
        "str": 23, "dex": 10, "con": 21, "int": 14, "wis": 11, "cha": 19,
        "saves": "Dex +4, Con +9, Wis +4, Cha +8",
        "skills": "Perception +8, Stealth +4",
        "damage_immunities": "fire",
        "challenge_rating": "10",
        "attacks": [
            {"name": "Bite", "bonus": 10, "damage": "2d10+6", "type": "piercing", "extra": "1d6 fire"},
            {"name": "Claw", "bonus": 10, "damage": "2d6+6", "type": "slashing"}
        ],
        "special": "Fire Breath (Recharge 5-6): The dragon exhales fire in a 30-foot cone. Each creature in that area must make a DC 17 Dexterity saving throw, taking 56 (16d6) fire damage on a failed save, or half as much damage on a successful one."
    },
    "skeleton": {
        "name": "Skeleton",
        "type": "Medium undead",
        "armor_class": 13,
        "hit_points": 13,
        "speed": "30 ft",
        "str": 10, "dex": 14, "con": 15, "int": 6, "wis": 8, "cha": 5,
        "damage_vulnerabilities": "bludgeoning",
        "damage_immunities": "poison",
        "condition_immunities": "exhaustion, poisoned",
        "challenge_rating": "1/4",
        "attacks": [
            {"name": "Shortsword", "bonus": 4, "damage": "1d6+2", "type": "piercing"},
            {"name": "Shortbow", "bonus": 4, "damage": "1d6+2", "type": "piercing", "range": "80/320 ft"}
        ]
    },
    "troll": {
        "name": "Troll",
        "type": "Large giant",
        "armor_class": 15,
        "hit_points": 84,
        "speed": "30 ft",
        "str": 18, "dex": 13, "con": 20, "int": 7, "wis": 9, "cha": 7,
        "skills": "Perception +2",
        "challenge_rating": "5",
        "attacks": [
            {"name": "Bite", "bonus": 7, "damage": "1d6+4", "type": "piercing"},
            {"name": "Claw", "bonus": 7, "damage": "2d6+4", "type": "slashing"}
        ],
        "special": "Regeneration: The troll regains 10 hit points at the start of its turn. If the troll takes acid or fire damage, this trait doesn't function at the start of the troll's next turn. The troll dies only if it starts its turn with 0 hit points and doesn't regenerate."
    }
}


def lookup_spell(spell_name: str) -> Dict[str, Any]:
    """Look up spell information by name"""
    spell_key = spell_name.lower().strip()
    
    if spell_key in SPELLS:
        return {
            "found": True,
            "spell": SPELLS[spell_key]
        }
    
    # Try partial match
    for key, spell in SPELLS.items():
        if spell_key in key or key in spell_key:
            return {
                "found": True,
                "spell": spell,
                "note": f"Found closest match: {spell['name']}"
            }
    
    return {
        "found": False,
        "error": f"Spell '{spell_name}' not found in database"
    }


def lookup_monster(monster_name: str) -> Dict[str, Any]:
    """Look up monster stats by name"""
    monster_key = monster_name.lower().strip()
    
    if monster_key in MONSTERS:
        return {
            "found": True,
            "monster": MONSTERS[monster_key]
        }
    
    # Try partial match
    for key, monster in MONSTERS.items():
        if monster_key in key or key in monster_key:
            return {
                "found": True,
                "monster": monster,
                "note": f"Found closest match: {monster['name']}"
            }
    
    return {
        "found": False,
        "error": f"Monster '{monster_name}' not found in database"
    }


def list_available_spells() -> List[str]:
    """List all available spells"""
    return [spell["name"] for spell in SPELLS.values()]


def list_available_monsters() -> List[str]:
    """List all available monsters"""
    return [monster["name"] for monster in MONSTERS.values()]


# Tool definitions for LLM
KNOWLEDGE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_spell",
            "description": "Look up detailed information about a D&D spell including damage, range, components, and description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "spell_name": {
                        "type": "string",
                        "description": "Name of the spell to look up (e.g., 'fireball', 'magic missile')"
                    }
                },
                "required": ["spell_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_monster",
            "description": "Look up detailed stats for a D&D monster including AC, HP, attacks, and special abilities.",
            "parameters": {
                "type": "object",
                "properties": {
                    "monster_name": {
                        "type": "string",
                        "description": "Name of the monster to look up (e.g., 'goblin', 'dragon', 'orc')"
                    }
                },
                "required": ["monster_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_available_spells",
            "description": "Get a list of all spells available in the database.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_available_monsters",
            "description": "Get a list of all monsters available in the database.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


TOOL_FUNCTIONS = {
    "lookup_spell": lookup_spell,
    "lookup_monster": lookup_monster,
    "list_available_spells": list_available_spells,
    "list_available_monsters": list_available_monsters
}
