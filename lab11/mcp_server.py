"""
DnD MCP Server - Lab 11
========================
YOUR TASK: Implement an MCP server with three DnD-related tools.

This server will expose tools that can be used by an LLM to interact
with a DnD game. Use the demo/simple_mcp_server.py as a reference.

Tools to implement:
1. roll_dice(n_dice, sides, modifier) - Roll dice and return the result
2. get_character_stat(character, stat) - Get a character's stat value
3. calculate_damage(base_damage, armor_class, attack_roll) - Calculate damage dealt
"""

import asyncio
import random
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


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

# =====================================================================
# TODO: Implement the three tool functions below.
# Each function should return a string with the result message.
# =====================================================================


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


# =====================================================================
# MCP Server wiring — tool schemas and call_tool dispatcher
# You should NOT need to modify anything below this line.
# =====================================================================

# Create the MCP server instance
server = Server("dnd-tools-server")

# Map tool names to their implementation functions
TOOL_FUNCTIONS = {
    "roll_dice": roll_dice,
    "get_character_stat": get_character_stat,
    "calculate_damage": calculate_damage,
}


@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available DnD tools.

    TODO: Define three tools with their input schemas:

    1. roll_dice:
       - n_dice (int): Number of dice to roll
       - sides (int): Number of sides on each die
       - modifier (int, optional): Modifier to add to the roll (default 0)

    2. get_character_stat:
       - character (str): Character name (fighter, wizard, or rogue)
       - stat (str): Stat name (strength, dexterity, constitution, intelligence, wisdom, charisma)

    3. calculate_damage:
       - base_damage (int): Base damage amount
       - armor_class (int): Target's armor class
       - attack_roll (int): The attack roll result

    See demo/simple_mcp_server.py for the Tool schema format.
    """
    return [
        # TODO: Define your tools here
        # Example:
        # Tool(
        #     name="roll_dice",
        #     description="Roll dice for DnD",
        #     inputSchema={
        #         "type": "object",
        #         "properties": {
        #             "n_dice": {"type": "integer", "description": "Number of dice"},
        #             ...
        #         },
        #         "required": ["n_dice", "sides"]
        #     }
        # ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Dispatch tool calls to the corresponding function."""
    func = TOOL_FUNCTIONS.get(name)
    if func is None:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    result = func(**arguments)
    return [TextContent(type="text", text=result)]


async def main():
    """Run the DnD MCP server."""
    import sys
    # Use stderr for logging since stdout is used for JSON-RPC protocol
    print("Starting DnD MCP server...", file=sys.stderr, flush=True)
    print("Tools: roll_dice, get_character_stat, calculate_damage", file=sys.stderr, flush=True)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
