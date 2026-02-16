# Prompt Engineering and Templates Lab

## Overview
This lab focuses on using prompt templates to drive a small, multi-agent DnD chat experience. You will wire up templates for a dungeon master (DM) and other encounters then orchestrate which agent to talk to based on the DM's response.

You will learn to use AgentTemplate class and create a branching conversation flow based on the DM's output.

## Files
- `demo.py` shows a minimal example of using a template to recruit an agent.
- `demo_template.json` is a small recruitable-agent template used by the demo.
- `lab04.py` contains the console chat driver and the places you must add logic.
- `lab04_dm.json`, `lab04_npc.json`, `lab04_enemy.json` are template files for the DM, NPC, and enemy given to you as a starting point.
- You can add, modify or delete the templates as you see fit. But you should have at least two different encounter templates for the DM to choose from.

## Lab Tasks
1. Inspect the provided templates and note which variables are expected (for example, `{{encounters}}` in the DM template).
2. Complete `run_console_chat()` in `lab04.py` so that, after the DM responds, the program decides which agent chat to start next.
3. Complete the `__main__` block in `lab04.py` to start the DM chat and pass the expected template parameters.
4. Run the script and verify that the conversation branches to the correct agent type based on the DM's output.

## Running
Run `lab04.py` directly to start the DM chat. The DM will select an encounter, and your logic should begin conversation with the appropriate agent.

## Grading
- **Functionality**: The DM chat starts correctly, and the program routes to the correct agent based on DM output.
- **Template Usage**: Template variables are provided and used correctly.