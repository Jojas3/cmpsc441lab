"""
Test script for Lab04
"""
import subprocess
import sys
from pathlib import Path

# Test Case 1: NPC Encounter
print("=" * 60)
print("Test Case 1: NPC Encounter")
print("=" * 60)

interactions_npc = [
    'What encounter do you have for me?',
    'I greet the NPC',
    'What quest do you have?',
    '/exit'
]

input_text = '\n'.join(interactions_npc)
subprocess.run([sys.executable, str(Path('lab04/lab04.py'))], input=input_text, text=True)

print("\n" + "=" * 60)
print("Test Case 2: Enemy Encounter")
print("=" * 60)

# Test Case 2: Enemy Encounter
interactions_enemy = [
    'What enemy shall I face?',
    'I draw my sword',
    'I attack the enemy',
    '/exit'
]

input_text = '\n'.join(interactions_enemy)
subprocess.run([sys.executable, str(Path('lab04/lab04.py'))], input=input_text, text=True)
