from .dndnetwork import DungeonMasterServer, PlayerClient
from .llm_utils import AgentTemplate
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama
import os


class OllamaEmbeddingFunction(chromadb.EmbeddingFunction):
    def __init__(self, model_name="nomic-embed-text"):
        self.model_name = model_name
    
    def __call__(self, input: List[str]) -> List[List[float]]:
        response = ollama.embed(self.model_name, input)
        return response['embeddings']


class DungeonMaster:
    def __init__(self):
        self.game_log = ['START']
        self.server = DungeonMasterServer(self.game_log, self.dm_turn_hook)
        self.chat = AgentTemplate.from_file('util/templates/dm_chat.json', sign='hello')
        self.start = True
        
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
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    chunks = text_splitter.split_text(content)
                    for i, chunk in enumerate(chunks):
                        documents.append(chunk)
                        ids.append(f"{os.path.basename(file_path)}_{i}")
                        metadatas.append({"source": file_path})
        
        if documents:
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )

    def start_server(self):
        self.server.start_server()

    def dm_turn_hook(self):
        dm_message = ''
        # Do DM things here. You can use self.game_log to access the game log
        
        # Get RAG context
        rag_context = self._get_rag_context()
        
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
            if msg.startswith("Player: "):
                last_action = msg[8:]  # Remove "Player: "
                break
        
        if not last_action:
            return ""
        
        # Query RAG
        try:
            results = self.collection.query(
                query_texts=[last_action],
                n_results=3
            )
            if results['documents']:
                context = "\n".join(results['documents'][0])
                return context
        except Exception as e:
            print(f"RAG query failed: {e}")
        
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
