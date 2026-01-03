import chromadb
from chromadb.utils import embedding_functions
import os

local_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path="./chroma_db")


collection = client.get_or_create_collection(
    name="portfolio_knowledge",
    embedding_function=local_ef
)

def add_to_knowledge_base(text, metadata, doc_id):
    """Adds a chunk of text to the vector database."""
    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[doc_id]
    )
    print(f"Added {doc_id} to knowledge base.")

def query_knowledge_base(query_text, n_results=3):
    """Searches for the most relevant context for a question."""
    return collection.query(
        query_texts=[query_text],
        n_results=n_results
    )