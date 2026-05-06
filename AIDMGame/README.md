# AI Dungeon Master Game

An AI-powered Dungeon Master game with multiplayer support, character management, RAG-enhanced storytelling, **and advanced AI features including tool calling, strategic AI, and multimodal output**.

## 🎯 Quick Start

```bash
# 1. Install dependencies
pip install ollama chromadb langchain-text-splitters pyttsx3

# 2. Start Ollama and pull model
ollama pull llama3.2

# 3. Start server
python AIDMGame/lab14.py server --host 127.0.0.1 --port 8000

# 4. Open browser
# Visit: http://127.0.0.1:8000/ui
```

**See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.**

## ✨ Advanced Features (NEW!)

### 🎲 Formal Tool Calling (16 Tools)
- **Dice Rolling**: Automatic d20 rolls, damage, saves, ability checks
- **Knowledge Lookup**: Spell and monster information retrieval
- **Text-to-Speech**: Dramatic narration for key moments
- **Image Generation**: ASCII art portraits and scenes
- **Strategic AI**: Intelligent enemy combat decisions

### 🧠 Chain-of-Thought Reasoning
- AI thinks step-by-step before responding
- Considers rules, difficulty, and outcomes
- More coherent and logical gameplay

### ⚔️ Strategic Enemy AI
- 4 intelligence levels (Berserker, Basic, Tactical, Mastermind)
- Enemies retreat, coordinate, and use tactics
- Target selection based on threat assessment

### 🎨 Multimodal Output
- Text responses (narrative, dialogue)
- Visual output (ASCII art)
- Audio output (text-to-speech)
- Structured data (dice rolls, stats)

**See [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md) for complete documentation.**

## 📁 Project Structure

```
AIDMGame/
├── lab14.py              # Main server and API handler
├── test_lab14.py         # Unit tests
├── Lab14.md              # Lab documentation
├── image.png             # Project screenshot
├── templates/
│   ├── dm_chat.json      # Original DM template
│   ├── dm_enhanced.json  # Enhanced DM with tool calling (NEW)
│   └── dm_combat.json    # Combat-focused template (NEW)
├── tools/                # Tool calling system (NEW)
│   ├── __init__.py       # Tool registry
│   ├── dice_tools.py     # Dice rolling (4 tools)
│   ├── knowledge_tools.py # Spell/monster lookup (4 tools)
│   ├── tts_tools.py      # Text-to-speech (1 tool)
│   └── image_tools.py    # Image generation (2 tools)
├── utils/
│   ├── __init__.py
│   ├── base.py           # DungeonMaster and Player classes (ENHANCED)
│   ├── dndnetwork.py     # Network server/client
│   ├── game.py           # Game runner
│   ├── llm_utils.py      # LLM utilities
│   ├── enhanced_llm.py   # Tool calling agent (NEW)
│   ├── player.py         # Player client
│   └── strategic_ai.py   # Enemy AI system (NEW)
├── data/                 # Game data directory
├── demo_advanced_features.py  # Feature demo (NEW)
├── test_advanced_features.py  # Feature tests (NEW)
├── QUICKSTART.md         # How to run (NEW)
├── ADVANCED_FEATURES.md  # Complete docs (NEW)
├── ENHANCEMENT_SUMMARY.md # What was added (NEW)
└── requirements_advanced.txt  # New dependencies (NEW)
```

## How to Run

### Quick Start

```bash
# Install dependencies
pip install ollama chromadb langchain-text-splitters pyttsx3

# Start Ollama
ollama pull llama3.2

# Test features (optional)
python AIDMGame/test_advanced_features.py
```

### Start the server
```bash
python AIDMGame/lab14.py server --host 127.0.0.1 --port 8000
```

### Join a session (in separate terminal)
```bash
python AIDMGame/lab14.py join --host 127.0.0.1 --port 8000 --session-id <id> --player-name <name>
```

### List available sessions
```bash
python AIDMGame/lab14.py list --host 127.0.0.1 --port 8000
```

### Access the web UI
Open your browser to: http://127.0.0.1:8000/ui

## Features

### Core Features
- Multiplayer game sessions
- Character creation and persistence (SQLite)
- AI Dungeon Master with RAG support
- Real-time game updates
- Web-based UI
- Turn-based combat system
- Character stats and inventory management

### Advanced AI Features (NEW!)
- **16 formal tools** for dice, knowledge, TTS, images, AI
- **Chain-of-thought reasoning** for better decisions
- **Strategic enemy AI** with 4 intelligence levels
- **Multimodal output** (text, audio, visual, data)
- **Automatic tool calling** by LLM
- **Enhanced prompts** for different scenarios

### Tool Categories
1. **Dice Rolling** (4 tools): roll_dice, roll_attack, roll_saving_throw, roll_ability_check
2. **Knowledge Lookup** (4 tools): lookup_spell, lookup_monster, list_spells, list_monsters
3. **Text-to-Speech** (1 tool): narrate_text with 3 voice types
4. **Image Generation** (2 tools): generate_npc_portrait, generate_scene_image
5. **Strategic AI** (1 tool): plan_enemy_actions

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - How to install and run
- **[ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)** - Complete feature documentation
- **[ENHANCEMENT_SUMMARY.md](ENHANCEMENT_SUMMARY.md)** - What was added and why
- **[FEATURE_CHECKLIST.md](FEATURE_CHECKLIST.md)** - Original feature list
