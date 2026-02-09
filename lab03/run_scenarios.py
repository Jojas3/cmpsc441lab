"""
Script to run the DnD agent multiple times with different interactions
Uses stdin to provide input automatically
"""
import subprocess
import sys
from pathlib import Path

# Define multiple interaction scenarios
scenarios = [
    {
        'name': 'Scenario 1: Combat Adventure',
        'interactions': [
            'Tell me about the adventure ahead of me.',
            'I decide to fight the monster!',
            'I use my magic spell to finish it.',
            '/exit'
        ]
    },
    {
        'name': 'Scenario 2: Stealth Mission',
        'interactions': [
            'What\'s my first challenge in this world?',
            'I try to sneak past the guards quietly.',
            'I search for treasure in the hidden chamber.',
            '/exit'
        ]
    },
    {
        'name': 'Scenario 3: Exploration Quest',
        'interactions': [
            'Begin my legendary adventure!',
            'I explore the mysterious forest.',
            'I investigate the old ruins I find.',
            '/exit'
        ]
    },
]

lab03_path = Path(__file__).parent / 'lab03_dnd_agent.py'

for scenario in scenarios:
    print(f"\n{'='*60}")
    print(f"Running: {scenario['name']}")
    print(f"{'='*60}\n")
    
    # Prepare input
    input_text = '\n'.join(scenario['interactions'])
    
    try:
        # Run the lab03_dnd_agent.py with input
        result = subprocess.run(
            [sys.executable, str(lab03_path)],
            input=input_text,
            text=True,
            capture_output=False,
            cwd=Path(__file__).parent
        )
        print(f"\nScenario completed with exit code: {result.returncode}\n")
    except Exception as e:
        print(f"Error running scenario: {e}\n")

print(f"\n{'='*60}")
print("All scenarios completed! Results saved to attempts.txt")
print(f"{'='*60}\n")
