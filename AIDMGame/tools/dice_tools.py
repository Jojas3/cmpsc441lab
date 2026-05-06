"""
Dice rolling tools for D&D mechanics
"""
import random
import re
from typing import Dict, Any


def roll_dice(notation: str) -> Dict[str, Any]:
    """
    Roll dice using standard D&D notation (e.g., '2d6', '1d20+5', '3d8-2')
    
    Args:
        notation: Dice notation string (e.g., '2d6', '1d20+5')
    
    Returns:
        Dictionary with roll results
    """
    # Parse notation like "2d6+3" or "1d20"
    pattern = r'(\d+)d(\d+)([+-]\d+)?'
    match = re.match(pattern, notation.lower().strip())
    
    if not match:
        return {"error": f"Invalid dice notation: {notation}"}
    
    num_dice = int(match.group(1))
    die_size = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    
    if num_dice > 100 or die_size > 1000:
        return {"error": "Dice values too large"}
    
    rolls = [random.randint(1, die_size) for _ in range(num_dice)]
    total = sum(rolls) + modifier
    
    return {
        "notation": notation,
        "rolls": rolls,
        "modifier": modifier,
        "total": total,
        "description": f"Rolled {notation}: {rolls} + {modifier} = {total}" if modifier else f"Rolled {notation}: {rolls} = {total}"
    }


def roll_attack(attack_bonus: int = 0) -> Dict[str, Any]:
    """Roll a d20 attack roll with bonus"""
    d20 = random.randint(1, 20)
    total = d20 + attack_bonus
    
    result = {
        "d20": d20,
        "bonus": attack_bonus,
        "total": total,
        "critical_hit": d20 == 20,
        "critical_miss": d20 == 1
    }
    
    if d20 == 20:
        result["description"] = f"CRITICAL HIT! Rolled natural 20 + {attack_bonus} = {total}"
    elif d20 == 1:
        result["description"] = f"CRITICAL MISS! Rolled natural 1"
    else:
        result["description"] = f"Attack roll: {d20} + {attack_bonus} = {total}"
    
    return result


def roll_saving_throw(ability_modifier: int = 0, advantage: bool = False, disadvantage: bool = False) -> Dict[str, Any]:
    """Roll a saving throw with optional advantage/disadvantage"""
    if advantage and disadvantage:
        advantage = disadvantage = False
    
    roll1 = random.randint(1, 20)
    
    if advantage or disadvantage:
        roll2 = random.randint(1, 20)
        d20 = max(roll1, roll2) if advantage else min(roll1, roll2)
        rolls = [roll1, roll2]
        adv_type = "advantage" if advantage else "disadvantage"
    else:
        d20 = roll1
        rolls = [roll1]
        adv_type = "normal"
    
    total = d20 + ability_modifier
    
    return {
        "rolls": rolls,
        "d20": d20,
        "modifier": ability_modifier,
        "total": total,
        "advantage_type": adv_type,
        "description": f"Saving throw ({adv_type}): {rolls} -> {d20} + {ability_modifier} = {total}"
    }


def roll_ability_check(skill_modifier: int = 0, dc: int = 10) -> Dict[str, Any]:
    """Roll an ability check against a DC"""
    d20 = random.randint(1, 20)
    total = d20 + skill_modifier
    success = total >= dc
    
    return {
        "d20": d20,
        "modifier": skill_modifier,
        "total": total,
        "dc": dc,
        "success": success,
        "description": f"Ability check: {d20} + {skill_modifier} = {total} vs DC {dc} - {'SUCCESS' if success else 'FAILURE'}"
    }


# Tool definitions for LLM
DICE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "roll_dice",
            "description": "Roll dice using D&D notation (e.g., '2d6', '1d20+5', '3d8-2'). Use this for damage rolls, random events, or any dice rolling.",
            "parameters": {
                "type": "object",
                "properties": {
                    "notation": {
                        "type": "string",
                        "description": "Dice notation like '2d6', '1d20+5', '3d8-2'"
                    }
                },
                "required": ["notation"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "roll_attack",
            "description": "Roll a d20 attack roll with an attack bonus. Returns whether it's a critical hit or miss.",
            "parameters": {
                "type": "object",
                "properties": {
                    "attack_bonus": {
                        "type": "integer",
                        "description": "Attack bonus to add to the d20 roll"
                    }
                },
                "required": ["attack_bonus"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "roll_saving_throw",
            "description": "Roll a saving throw with optional advantage or disadvantage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ability_modifier": {
                        "type": "integer",
                        "description": "Ability modifier to add to the roll"
                    },
                    "advantage": {
                        "type": "boolean",
                        "description": "Whether to roll with advantage (roll twice, take higher)"
                    },
                    "disadvantage": {
                        "type": "boolean",
                        "description": "Whether to roll with disadvantage (roll twice, take lower)"
                    }
                },
                "required": ["ability_modifier"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "roll_ability_check",
            "description": "Roll an ability check (like Perception, Stealth, Persuasion) against a difficulty class (DC).",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill_modifier": {
                        "type": "integer",
                        "description": "Skill modifier to add to the d20 roll"
                    },
                    "dc": {
                        "type": "integer",
                        "description": "Difficulty Class (DC) to beat"
                    }
                },
                "required": ["skill_modifier", "dc"]
            }
        }
    }
]


# Map function names to actual functions
TOOL_FUNCTIONS = {
    "roll_dice": roll_dice,
    "roll_attack": roll_attack,
    "roll_saving_throw": roll_saving_throw,
    "roll_ability_check": roll_ability_check
}
