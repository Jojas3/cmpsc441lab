from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))

from ollama import chat
from util.llm_utils import pretty_stringify_chat, ollama_seed as seed

# Add you code below
sign_your_name = 'GitHub Copilot'
model = 'gemma3:270m'
options = {'temperature': 0.7, 'top_p': 0.9}
messages = [
  {'role': 'system', 'content': 'You are an experienced and creative Dungeon Master running a D&D adventure. You create immersive and engaging fantasy worlds with vivid descriptions. You are friendly, enthusiastic, and always ready to respond to player actions. Guide the player through an exciting adventure full of mystery, danger, and discovery.'}
]

# But before here.
messages.append({'role':'user', 'content':'Start an epic D&D adventure for me!'}) # An empty user message to prompt the model to start responding.

options |= {'seed': seed(sign_your_name)}
# Chat loop
while True:
  response = chat(model=model, messages=messages, stream=False, options=options)
  # Add your code below
  assistant_message = response.message.content
  messages.append({'role': 'assistant', 'content': assistant_message})
  print(f'Dungeon Master: {assistant_message}\n')
  
  user_input = input('You: ')
  messages.append({'role': 'user', 'content': user_input})

  # But before here.
  if user_input == '/exit':
    break

# Save chat
with open(Path('lab03/attempts.txt'), 'a') as f:
  file_string  = ''
  file_string +=       '-------------------------NEW ATTEMPT-------------------------\n\n\n'
  file_string += f'Model: {model}\n'
  file_string += f'Options: {options}\n'
  file_string += pretty_stringify_chat(messages)
  file_string += '\n\n\n------------------------END OF ATTEMPT------------------------\n\n\n'
  f.write(file_string)

