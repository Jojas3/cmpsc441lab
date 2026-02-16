from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parents[1]))

from util.llm_utils import AgentTemplate

# Sign your name here
sign_your_name = 'Jacob Dzikowski'

# Get the lab04 directory
lab04_dir = Path(__file__).parent

def run_console_chat(template_file, agent_name='Agent', **kwargs):
    '''
    Run a console chat with the given template file and agent name.
    Args:
        template_file: The path to the template file.
        agent_name: The name of the agent to display in the console.
        **kwargs: Additional arguments to pass to the AgentTemplate.from_file method.
    '''
    chat = AgentTemplate.from_file(template_file, **kwargs)
    response = chat.start_chat()
    while True:
        print(f'{agent_name}: {response}')
        try:
            response = chat.send(input('You: '))
            # Check if DM response indicates we should switch agents
            response_lower = response.lower()
            if 'npc' in response_lower or 'friendly' in response_lower or 'quest' in response_lower:
                # Switch to NPC agent
                print('\n--- Switching to NPC encounter ---\n')
                npc_chat = run_console_chat(lab04_dir / 'lab04_npc.json', agent_name='NPC')
                return npc_chat
            elif 'enemy' in response_lower or 'hostile' in response_lower or 'combat' in response_lower or 'battle' in response_lower:
                # Switch to Enemy agent
                print('\n--- Switching to Enemy encounter ---\n')
                enemy_chat = run_console_chat(lab04_dir / 'lab04_enemy.json', agent_name='Enemy')
                return enemy_chat
        except StopIteration as e:
            break

if __name__ ==  '__main__':
    # Start DM chat with encounters list as parameter
    encounters = 'a friendly NPC (quest-giver) or a hostile Enemy (dragon)'
    run_console_chat(lab04_dir / 'lab04_dm.json', 
                     agent_name='Dungeon Master',
                     encounters=encounters)