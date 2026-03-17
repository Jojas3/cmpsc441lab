#!/usr/bin/env python3
"""
RAG (Retrieval-Augmented Generation) Demo Script
Using ChromaDB for vector storage, chunking, and Ollama for both embeddings and LLM generation
"""

import os
import glob
import time
from typing import List, Dict, Any

# Vector database, embedding, and text processing
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter


import ollama
import numpy as np

# Utility imports
import pandas as pd


class OllamaEmbeddingFunction(chromadb.EmbeddingFunction):
    """
    Custom embedding function that uses Ollama for embeddings.
    
    Inputs:
        model_name (str): Name of the Ollama embedding model to use.
    Outputs:
        Callable that takes a list of strings and returns a list of embedding vectors (List[List[float]]).
    """
    
    def __init__(self, model_name="nomic-embed-text"):
        self.model_name = model_name
    
    def __call__(self, input: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Ollama.
        
        Inputs:
            input (List[str]): List of text strings to embed.
        Outputs:
            List[List[float]]: List of embedding vectors, one per input string.
        """
        pass


def load_documents(data_dir: str) -> Dict[str, str]:
    """
    Load text documents from a directory.
    
    Inputs:
        data_dir (str): Path to the directory containing .txt files.
    Outputs:
        Dict[str, str]: Dictionary mapping filename to file content as a string.
    """
    documents = {}
    for file_path in glob.glob(os.path.join(data_dir, "*.txt")):
        with open(file_path, 'r') as file:
            content = file.read()
            documents[os.path.basename(file_path)] = content
    
    print(f"Loaded {len(documents)} documents from {data_dir}")
    return documents


def chunk_documents(documents: Dict[str, str], chunk_size: int = 500, chunk_overlap: int = 50) -> List[Dict[str, Any]]:
    """
    Split documents into smaller chunks for embedding using LangChain's RecursiveCharacterTextSplitter.
    
    Inputs:
        documents (Dict[str, str]): Dictionary mapping filename to file content.
        chunk_size (int): Maximum size of each chunk (default 500).
        chunk_overlap (int): Number of overlapping characters between chunks (default 50).
    Outputs:
        List[Dict[str, Any]]: List of chunk dictionaries with 'id', 'text', and 'metadata'.
    """
    chunked_documents = []
    
    # Create the chunker with specified parameters
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    
    for doc_name, content in documents.items():
        # Apply the chunker to the document text
        
        chunks = text_splitter.split_text(content)
        
        for i, chunk in enumerate(chunks):
            chunked_documents.append({
                "id": f"{doc_name}_chunk_{i}",
                "text": chunk,
                "metadata": {"source": doc_name, "chunk": i}
          })
    
    print(f"Created {len(chunked_documents)} chunks from {len(documents)} documents")
    return chunked_documents


def setup_chroma_db(chunks: List[Dict[str, Any]], collection_name: str = "dnd_knowledge", use_ollama_embeddings: bool = True, ollama_model: str = "nomic-embed-text") -> chromadb.Collection:
    """
    Set up ChromaDB with document chunks and add them to a collection.
    
    Inputs:
        chunks (List[Dict[str, Any]]): List of chunk dictionaries with 'id', 'text', and 'metadata'.
        collection_name (str): Name of the ChromaDB collection (default 'dnd_knowledge').
        use_ollama_embeddings (bool): Whether to use Ollama for embeddings (default True).
        ollama_model (str): Name of the Ollama embedding model (default 'nomic-embed-text').
    Outputs:
        chromadb.Collection: The created ChromaDB collection with added chunks.
    """
    # Initialize ChromaDB Ephemeral client
    client = chromadb.Client()
    # Initialize ChromaDB Persistent client
    #client = chromadb.PersistentClient(path="/path/to/save/to")
    
    # Create embedding function
    # Use custom Ollama embedding function
    embedding_function = OllamaEmbeddingFunction(model_name=ollama_model)
    print(f"Using Ollama for embeddings with model: {ollama_model}")
    
    # Create or get collection
    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )
    
    # Add documents to collection
    collection.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[chunk["metadata"] for chunk in chunks]
    )
    
    print(f"Added {len(chunks)} chunks to ChromaDB collection '{collection_name}'")
    return collection


def retrieve_context(collection: chromadb.Collection, query: str, n_results: int = 3) -> List[str]:
    """
    Retrieve relevant context from ChromaDB based on the query.
    
    Inputs:
        collection (chromadb.Collection): The ChromaDB collection to search.
        query (str): The user query string.
        n_results (int): Number of top relevant results to retrieve (default 3).
    Outputs:
        List[str]: List of retrieved context strings relevant to the query.
    """
    pass



def generate_response(query: str, contexts: List[str], model: str = "mistral:latest") -> str:
    """
    Generate a response using Ollama LLM with the retrieved context.
    
    Inputs:
        query (str): The user query string.
        contexts (List[str]): List of context strings to include in the prompt.
        model (str): Name of the Ollama LLM model to use (default 'mistral:latest').
    Outputs:
        str: The generated response from the LLM.
    """
    # Create prompt with context
    context_text = "\n\n".join(contexts)
    
    prompt = f"""You are a helpful assistant for Dungeons & Dragons players.
    Use the following information to answer the question.
    
    Context:
    {context_text}
    
    Question: {query}
    
    Answer:"""
    
    response = ollama.generate(
        model=model,
        prompt=prompt,
    )
    
    return response["response"]


def display_results(query: str, contexts: List[str], response: str) -> None:
    """
    Display the query, context, and generated response in a formatted way.
    
    Inputs:
        query (str): The user query string.
        contexts (List[str]): List of context strings used for generation.
        response (str): The generated response from the LLM.
    Outputs:
        None
    """
    print("\n" + "="*80)
    print(f"QUERY: {query}")
    print("="*80)
    
    print("\nCONTEXT USED:")
    print("-"*80)
    for i, context in enumerate(contexts, 1):
        print(f"Context {i}:")
        print(context[:200] + "..." if len(context) > 200 else context)
        print()
    
    print("\nGENERATED RESPONSE:")
    print("-"*80)
    print(response)
    print("="*80 + "\n")


def main():
    """
    Main function to run the RAG demo
    """
    
    # Set embedding and LLM models
    embedding_model = "nomic-embed-text"  # Change to your preferred embedding model
    llm_model = "llama3.2:latest"  # Change to your preferred LLM model
    
    # 1. Load documents
    data_dir = "lab08/data"
    documents = load_documents(data_dir)
    
    # 2. Chunk documents using ChromaDB chunker
    chunks = chunk_documents(documents)
    
    # 3. Set up ChromaDB with Ollama embeddings
    collection = setup_chroma_db(
        chunks, 
        ollama_model=embedding_model
    )
    
    # 4. Example queries
    queries = [
        "What abilities do wizards have in D&D?",
        "Explain how a Bag of Holding works.",
        "What happens if you roll a 20 with a Vorpal Sword?",
        "Compare the abilities of fighters and rogues."
    ]
    
    # 5. Run RAG for each query
    for query in queries:
        # Retrieve context
        contexts = retrieve_context(collection, query)
        
        # Generate response
        response = generate_response(query, contexts, model=llm_model)
        
        # Display results
        display_results(query, contexts, response)
    

if __name__ == "__main__":
    main() 
