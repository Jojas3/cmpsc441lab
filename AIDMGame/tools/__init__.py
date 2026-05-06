"""
Tools package for AI Dungeon Master
Provides dice rolling and knowledge lookup
"""
from .dice_tools import DICE_TOOLS, TOOL_FUNCTIONS as DICE_FUNCTIONS
from .knowledge_tools import KNOWLEDGE_TOOLS, TOOL_FUNCTIONS as KNOWLEDGE_FUNCTIONS
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.strategic_ai import STRATEGIC_AI_TOOLS, TOOL_FUNCTIONS as AI_FUNCTIONS


# Combine all tools
ALL_TOOLS = DICE_TOOLS + KNOWLEDGE_TOOLS + STRATEGIC_AI_TOOLS

# Combine all tool functions
ALL_TOOL_FUNCTIONS = {
    **DICE_FUNCTIONS,
    **KNOWLEDGE_FUNCTIONS,
    **AI_FUNCTIONS
}


__all__ = [
    'ALL_TOOLS',
    'ALL_TOOL_FUNCTIONS',
    'DICE_TOOLS',
    'KNOWLEDGE_TOOLS'
]
