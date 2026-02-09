# Prompt Engineering Process

## Step 1: Initial Implementation with Basic System Prompt

### Intention
Create a functional D&D agent with a basic system prompt that establishes the Dungeon Master role and implements the core chat loop structure based on demo_agent.py.

### Action/Change
- Implemented the main chat loop: display assistant response, get user input, check for /exit command
- Added initial system prompt: "You are an experienced and creative Dungeon Master running a D&D adventure. You create immersive and engaging fantasy worlds with vivid descriptions. You are friendly, enthusiastic, and always ready to respond to player actions. Guide the player through an exciting adventure full of mystery, danger, and discovery."
- Set temperature to 0.7 and top_p to 0.9 for balanced creativity
- Used model: gemma3:270m

### Result
The agent successfully initiates conversations and responds to player actions. The system prompt establishes context, but responses can be somewhat generic without detailed world-building or consequences.

### Reflection/Analysis of the Result
The basic setup works well for getting started, but the generic system prompt doesn't provide specific constraints or narrative hooks that would make the adventure more engaging. The temperature settings are reasonable for creativity, but may need adjustment based on desired response coherence.

---

## Step 2: Enhanced System Prompt with World Context

### Intention
Improve engagement by providing a specific fantasy world setting and establishing clearer expectations for the DM's behavior regarding consequences and narrative flow.

### Action/Change
Updated system prompt to include:
- Specific world setting: "You are running an adventure in a dark, mysterious realm filled with ancient magic"
- Consequences emphasis: "Remember that every player action has consequences that affect the story"
- Engagement hooks: "Create interesting NPCs with unique personalities and motivations"
- Story progression: "Guide the narrative toward meaningful encounters and decisions"
- Modified temperature to 0.8 for increased creativity while maintaining coherence

### Result
The agent provides more contextually relevant responses that reference specific world elements and creates named NPCs. Responses feel more immersive with better narrative continuity.

### Reflection/Analysis of the Result
The enhanced world context significantly improves immersion. By explicitly mentioning consequences and specific world details, the model generates more engaging narratives. The slightly higher temperature allows for more varied responses while the explicit instructions help maintain narrative consistency. This iteration clearly improved the player experience.

---

## Step 3: Constraint-Based Prompt for Focused Gameplay

### Intention
Test whether adding explicit gameplay constraints and rules helps the agent make better decisions about story pacing and player challenges.

### Action/Change
- Added explicit mechanics: "Manage character resources (health, spells, items) and describe their current status"
- Added pacing guidance: "Present meaningful choices rather than just narrating events"
- Added challenge management: "Balance difficulty - challenges should be hard but fair, with realistic odds shown to the player"
- Reduced temperature to 0.6 to prioritize rule consistency over pure creativity
- Added max_tokens constraint of 200 for more focused responses

### Result
The agent becomes more structured in presenting information and tends to explicitly offer choices. Responses are more concise and game-like rather than purely narrative. However, some creative flourishes are lost.

### Reflection/Analysis of the Result
The constraints made the gameplay more interactive and clear about available options. The lower temperature improved consistency but made responses somewhat formulaic. The max_tokens limit was effective for pacing but sometimes cut off interesting descriptions. This shows a tradeoff between structure and immersion - both are valuable depending on the player's preference.

---

## Step 4: Emotional Depth and Player Investment

### Intention
Enhance player engagement by making NPCs and situations more emotionally compelling and creating personal stakes in the story.

### Action/Change
- Added emotional guidance: "Create emotionally resonant NPCs that the player can form relationships with"
- Added stakes: "Make the consequences of player choices matter - victories should feel earned and failures should hurt"
- Added player investment: "Create situations where the player's character decisions reveal their personality and values"
- Increased temperature back to 0.75 for more nuanced emotional responses
- Removed max_tokens limit to allow fuller narrative descriptions

### Result
The agent creates more compelling story moments with named NPCs that have apparent motivations and emotional arcs. Players report feeling more invested in the narrative outcomes.

### Reflection/Analysis of the Result
This iteration significantly improved narrative engagement by focusing on emotional investment. The removal of hard token limits allowed for richer descriptions while the emotional guidance created more memorable encounters. The moderate temperature provided good balance between creative storytelling and coherent world-building. This proved to be one of the most impactful changes for player experience.

---

## Step 5: Meta-Gaming and Adaptability

### Intention
Improve the agent's ability to adapt to individual play styles and learn from player preferences throughout a session.

### Action/Change
- Added adaptability: "Pay attention to what the player enjoys - more combat, exploration, roleplay, or problem-solving - and adapt the scenario to their preferences"
- Added tone matching: "Mirror the player's communication style and match their desired tone (serious, comedic, dark, whimsical, etc.)"
- Added flexibility: "Be willing to deviate from planned narrative if the player takes an interesting direction"
- Set temperature to 0.8 with seed randomization for reproducibility while maintaining variation
- Added session tracking reminder: "Remember all previous events and character development from this adventure"

### Result
The agent becomes more responsive to individual player preferences and adjusts pacing/tone accordingly. Sessions feel more personalized. The agent maintains better continuity of character development and world state.

### Reflection/Analysis of the Result
This iteration demonstrated that meta-awareness about the gaming experience itself improves player satisfaction. By explicitly instructing the model to observe and adapt to player preferences, the agent becomes less one-size-fits-all and more tailored. The seed consistency with high temperature provides good reproducibility for testing while maintaining freshness. This iteration shows that flexibility and responsiveness are key components of good game facilitation.

---

## Key Learnings

1. **System prompts matter significantly** - Moving from generic to specific world context improved immersion dramatically
2. **Temperature tuning requires thoughtful tradeoffs** - Higher temperatures enable creativity but lower temperatures improve consistency
3. **Explicit instruction of values** - Telling the model what matters (consequences, emotional investment, player agency) directly affects output quality
4. **Player-centric design** - The best improvements focused on what makes the player experience better rather than what seems technically impressive
5. **Iterative refinement** - Each iteration built on previous learnings, showing that systematic experimentation is more effective than random changes
