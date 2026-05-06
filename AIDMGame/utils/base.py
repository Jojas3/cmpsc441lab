from .dndnetwork import DungeonMasterServer, PlayerClient
from .llm_utils import AgentTemplate
from .enhanced_llm import ToolCallingAgent, MultiModalAgent
from typing import List
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama
import os
import sys
import json

# Add tools to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tools import ALL_TOOLS, ALL_TOOL_FUNCTIONS


class OllamaEmbeddingFunction(chromadb.EmbeddingFunction):
    def __init__(self, model_name="nomic-embed-text"):
        self.model_name = model_name
    
    def __call__(self, input: List[str]) -> List[List[float]]:
        response = ollama.embed(self.model_name, input)
        return response['embeddings']


class DungeonMaster:
    def __init__(self, use_enhanced: bool = True):
        self.game_log = ['START']
        self.server = DungeonMasterServer(self.game_log, self.dm_turn_hook)
        self.use_enhanced = use_enhanced
        
        # Use enhanced agent with tool calling
        if use_enhanced:
            template_path = 'AIDMGame/templates/dm_enhanced.json'
            if not os.path.exists(template_path):
                template_path = 'AIDMGame/templates/dm_chat.json'
            self.agent = MultiModalAgent(template_path, ALL_TOOLS, ALL_TOOL_FUNCTIONS)
            print("[DM] Enhanced AI with tool calling enabled")
            print(f"[DM] Available tools: {len(ALL_TOOLS)}")
        else:
            self.chat = AgentTemplate.from_file('AIDMGame/templates/dm_chat.json', sign='hello')
        
        self.start = True
        self.combat_mode = False
        self.planning_enabled = True
        
        # Setup RAG
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_function = OllamaEmbeddingFunction()
        self.collection = self.chroma_client.get_or_create_collection(
            name="dnd_knowledge",
            embedding_function=self.embedding_function
        )
        
        # Load and chunk D&D data if collection is empty
        if self.collection.count() == 0:
            self._load_dnd_data()
        
    def _load_dnd_data(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        
        data_files = [
            "lab08/data/dnd_character_classes.txt",
            "lab08/data/dnd_magic_items.txt"
        ]
        
        documents = []
        ids = []
        metadatas = []
        
        for file_path in data_files:
            if os.path.exists(file_path):
                print(f"[RAG] Loading {file_path}...")
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    chunks = text_splitter.split_text(content)
                    for i, chunk in enumerate(chunks):
                        documents.append(chunk)
                        ids.append(f"{os.path.basename(file_path)}_{i}")
                        metadatas.append({"source": file_path})
                print(f"[RAG] Loaded {len(chunks)} chunks from {file_path}")
            else:
                print(f"[RAG] Warning: {file_path} not found, skipping...")
        
        if documents:
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            print(f"[RAG] Total documents in collection: {self.collection.count()}")
        else:
            print("[RAG] Warning: No D&D data files found. RAG will not be available.")

    def start_server(self):
        self.server.start_server()

    def dm_turn_hook(self):
        dm_message = ''
        
        # Get RAG context
        rag_context = self._get_rag_context()
        
        if self.use_enhanced:
            # Use enhanced agent with tool calling
            if self.start:
                prompt = "Welcome the players to an epic D&D adventure! Set the scene dramatically and ask what they'd like to do."
                self.start = False
            else:
                # Build context-rich prompt
                recent_log = '\n'.join(self.game_log[-10:])  # Last 10 entries
                
                # Check if last action is character management
                last_action = self.game_log[-1] if self.game_log else ""
                is_char_management = any(keyword in last_action.lower() for keyword in 
                    ['inventory', 'add', 'remove', 'class', 'change', 'stat', 'level', 'equipment'])
                
                prompt = f"Game Log:\n{recent_log}\n\n"
                
                if rag_context:
                    prompt += f"Relevant D&D Knowledge:\n{rag_context}\n\n"
                
                # Add strategic guidance
                if is_char_management:
                    prompt += "The player is requesting a character change. Narrate the change happening in-world, confirm what changed, and continue the adventure.\n\n"
                elif self.combat_mode:
                    prompt += "You are in combat mode. Use tactical AI to control enemies intelligently. Use roll_attack and roll_dice tools.\n\n"
                
                prompt += "Respond as the Dungeon Master. Use tools when appropriate (dice rolls, lookups). For character changes, narrate them directly without tools."
            
            # Get response with tool calling
            result = self.agent.process_action(prompt)
            dm_message = result['text']
            
            # Log any tool usage
            if result['tool_calls']:
                print(f"[DM] Used {len(result['tool_calls'])} tools")
                for tool_call in result['tool_calls']:
                    if 'description' in tool_call:
                        print(f"[DM] {tool_call['description']}")
            
            # Display any ASCII art
            if result['images']:
                for img in result['images']:
                    print(f"\n{img}\n")
                    dm_message += f"\n\n[Visual generated - see console]\n"
        else:
            # Use legacy agent
            if self.start:
                dm_message = self.chat.start_chat()
                self.start = False
            else: 
                prompt = '\n'.join(self.game_log)
                if rag_context:
                    prompt = f"Relevant D&D knowledge:\n{rag_context}\n\n{prompt}"
                dm_message = self.chat.send(prompt)

        # Return a message to send to the players for this turn
        return dm_message
    
    def _get_rag_context(self):
        # Find the last player action
        last_action = None
        for msg in reversed(self.game_log):
            # Check for player actions in format "PlayerName: action"
            if msg and not msg.startswith("DM:") and not msg.startswith("START"):
                # Extract just the action part after the player name
                if ": " in msg:
                    last_action = msg.split(": ", 1)[1]
                else:
                    last_action = msg
                break
        
        if not last_action:
            return ""
        
        # Query RAG
        try:
            results = self.collection.query(
                query_texts=[last_action],
                n_results=3
            )
            if results['documents'] and results['documents'][0]:
                context = "\n\n".join(results['documents'][0])
                print(f"[RAG] Query: {last_action}")
                print(f"[RAG] Found {len(results['documents'][0])} relevant chunks")
                return context
        except Exception as e:
            print(f"[RAG] Query failed: {e}")
        
        return "" 


class Player:
    def __init__(self, name):
        self.name = name
        self.client = PlayerClient(self.name)

    def connect(self):
        self.client.connect()

    def unjoin(self):
        self.client.unjoin()

    def take_turn(self, message):
        self.client.send_message(message)
