# Lab03: LLM Agent Development - Reflection Report

## Overview
This lab involved creating a D&D Dungeon Master agent using the Ollama LLM framework. The agent was implemented in `lab03_dnd_agent.py` and tested with multiple interactive scenarios.

---

## Step 1: Initial Implementation

### Intention
Implement a working D&D Dungeon Master agent that can conduct a conversation with a player, maintaining message history and gracefully handling session exits.

### Action/Change
- Created a chat-based system using the `ollama` library with the `gemma3:270m` model
- Implemented message history management with system prompt, user messages, and assistant responses
- Set model parameters: temperature=0.7, top_p=0.9
- Added system prompt to define the DM character: an experienced, creative Dungeon Master
- Implemented `/exit` command to gracefully terminate the conversation

### Result
The agent successfully initialized and maintained conversations through multiple turns. The agent responded coherently to player actions and questions, creating an engaging D&D narrative experience.

### Reflection/Analysis of the Result
The implementation was successful due to:
- **Clear system prompt**: The system message effectively guided the model to roleplay as a DM
- **Message structure**: Properly formatted messages (system, user, assistant) helped maintain conversation context
- **Seed parameter**: Using a deterministic seed based on the user's name ensured reproducibility
- **Temperature setting**: A moderate temperature (0.7) balanced creativity with stability

The agent demonstrated good narrative coherence and responded appropriately to player actions. The use of Eldoria as the setting was consistent across sessions.

---

## Step 2: Multiple Scenario Testing

### Intention
Test the agent's consistency and robustness across multiple different interaction scenarios to verify it can handle varied player inputs and maintain the D&D narrative.

### Action/Change
- Created `run_scenarios.py` to automate running the agent three times with different interaction sequences
- Scenario 1: Combat-focused adventure with monster fighting and spell casting
- Scenario 2: Stealth-focused adventure with guard sneaking and treasure hunting
- Scenario 3: Exploration-focused adventure with forest exploration and ruins investigation
- Each scenario properly calls `/exit` to gracefully close the session and save attempts

### Result
All three scenarios completed successfully with exit code 0. The agent:
- Consistently created engaging narratives
- Responded appropriately to different player approaches (combat, stealth, exploration)
- Maintained character as the Dungeon Master throughout each session
- Properly saved all session data to `attempts.txt`

### Reflection/Analysis of the Result
The agent showed strong robustness and consistency:
- **Adaptability**: The agent adapted well to different player strategies without losing the DM role
- **Context awareness**: Each response built on the player's previous actions
- **Consistent tone**: Despite different scenarios, the agent maintained the same enthusiastic, narrative-driven tone
- **File persistence**: The `attempts.txt` file successfully accumulated session data from all three runs
- **Seed reproducibility**: The fixed seed ensured consistent initial responses across runs

The agent successfully demonstrated that it can handle multiple complete game sessions while maintaining narrative quality and proper session management.

---

## Step 3: Code Quality and Structure

### Intention
Ensure the implementation follows best practices and the code is well-structured for maintainability.

### Action/Change
- Code includes proper imports and path setup for accessing utility modules
- Uses `pretty_stringify_chat()` function to format chat history for logging
- Implements `ollama_seed()` function to generate deterministic seeds from user names
- Proper file handling with append mode for `attempts.txt`
- Clear separation between configuration (model, options) and execution logic

### Result
The code is clean, functional, and properly structured. All required functionality works as intended.

### Reflection/Analysis of the Result
The implementation benefits from:
- **Modular design**: Utility functions in `util/llm_utils.py` reduce code duplication
- **Reproducibility**: Seed-based randomization allows for testing and debugging
- **Proper logging**: All sessions are appended to a single file for review
- **Error handling**: The `/exit` command properly terminates the loop and saves data

---

## Key Observations

1. **Model Performance**: The `gemma3:270m` model is lightweight but effective for D&D narration
2. **Temperature Setting**: The 0.7 temperature provides good balance between creativity and coherence
3. **System Prompt Effectiveness**: A detailed system prompt significantly improves role adherence
4. **Session Management**: Graceful exit handling and proper file logging enables session persistence

---

## Conclusion

The lab successfully demonstrates the implementation of a working LLM-based agent that can:
- Maintain conversation context over multiple turns
- Generate coherent, narrative-driven responses
- Adapt to different player actions and strategies
- Gracefully handle session termination and logging

The agent is functional, consistent, and ready for use. The multiple test scenarios confirm its robustness across different interaction patterns.
