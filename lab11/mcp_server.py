"""
DnD MCP Server - Lab 11
===================================
Complete implementation of the MCP server with three DnD-related tools.
"""

import random
from fastmcp import FastMCP


# Sample character data - use this for get_character_stat
CHARACTERS = {
    "fighter": {
        "strength": 16,
        "dexterity": 14,
        "constitution": 15,
        "intelligence": 10,
        "wisdom": 12,
        "charisma": 8
    },
    "wizard": {
        "strength": 8,
        "dexterity": 14,
        "constitution": 12,
        "intelligence": 18,
        "wisdom": 15,
        "charisma": 10
    },
    "rogue": {
        "strength": 10,
        "dexterity": 18,
        "constitution": 12,
        "intelligence": 14,
        "wisdom": 10,
        "charisma": 14
    }
}

# Create the MCP server instance
mcp = FastMCP("dnd-tools-server")

@mcp.tool()
def roll_dice(n_dice: int, sides: int, modifier: int = 0) -> str:
    """
    Roll n_dice dice with the given number of sides, plus a modifier.

    TODO:
    - Roll each die using random.randint(1, sides)
    - Sum the rolls and add the modifier
    - Return a message like "Rolled 3d6+2: [4, 2, 5] + 2 = 13"
    """
    # TODO: Implement dice rolling
    pass


@mcp.tool()
def get_character_stat(character: str, stat: str) -> str:
    """
    Look up a character's stat from the CHARACTERS dict.

    TODO:
    - Normalize character and stat to lowercase
    - Look up the character in CHARACTERS
    - Return the stat value, e.g. "Fighter's strength is 16"
    - Handle invalid character/stat names gracefully
    """
    # TODO: Implement character stat lookup
    pass


@mcp.tool()
def calculate_damage(base_damage: int, armor_class: int, attack_roll: int) -> str:
    """
    Calculate damage dealt based on attack roll vs armor class.

    TODO:
    - If attack_roll >= armor_class, the attack hits (return base_damage info)
    - Otherwise, the attack misses (0 damage)
    - Return a descriptive message
    """
    # TODO: Implement damage calculation
    pass


if __name__ == "__main__":
    mcp.run(transport="stdio")
