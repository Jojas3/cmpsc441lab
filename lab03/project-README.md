# Course Project: AI DnD Dungeon Master

## Intro to the Course Project
Create an AI based DnD Dungeon Master (DM) to allow you to play DnD with your friends without needing someone to be a DM. The Dungeon Master will be able to generate a story, create NPC characters, manage the game world, and make appropriate changes to the player character sheets. The project will be broken down into several milestones, each building on the previous one to create a fully functional DnD Dungeon Master.

Note: This project is designed to be a fun and interactive way to apply the concepts you have learned in the course. Feel free to get creative and experiment with different ideas to enhance the project.

Note: You are free to not use DnD as the theme for your project. You can make it a general text-based adventure game if you prefer or something else entirely. But the project should use all the technologies that are expected in the project. Look at the project rubric for more details.

## Capabilities of the DnD Dungeon Master
1. Generate a random story
2. Take the players on an adventure in the fantasy world of DnD.
2. Create NPC characters
3. Manage the game world
4. Make changes to player character sheets
5. Implement a turn-based combat system

##  Scaffolding
As a part of lab03 you are provided with a basic scaffolding for the project. The scaffolding includes the following:

1. Networked game server and client (Dungeon Master Server and Player Client) `utils/dndnetwork.py`
2. Chat template for a DnD llm agent `utils/templates/dm_chat.json`
3. A basic DungeonMaster and Player class that allow you to use the networked game server and client `utils/base.py`

## Using UV for Project

UV is a modern Python package manager that's faster than pip and handles virtual environments automatically.

**Install UV:** https://docs.astral.sh/uv/getting-started/installation/
```cmd
#CMD install
C:\>winget install --id=astral-sh.uv  -e
```

```bash
# Initialize project (creates pyproject.toml)
uv init

# Add packages for your lab
uv add requests numpy pandas

# Run your lab code with dependencies
uv run python lab03.py

# Install all project dependencies
uv sync
```

UV ensures consistent Python versions and dependencies across all lab environments.

### VSCode setup for uv
After you have installed uv and ran `uv sync` to ensure a virtual environment is created, you can set the python interpreter to uv virtual env.

- Click on the Python Interpreter on the bottom right of the VSCode window. (Ensure a python file is currently active for the button to appear.)

- Set it to the path `.\.venv\Scripts\python.exe`