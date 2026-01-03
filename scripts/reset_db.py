import chromadb
from scripts.database import collection
import os

def reset_and_chunk_cv():
    print("Clearing old database entries...")
    all_ids = collection.get()['ids']
    if all_ids:
        collection.delete(ids=all_ids)

    with open("data/processed/cv.md", "r") as f:
        content = f.read()

    chunks = [c.strip() for c in content.split("\n\n") if len(c.strip()) > 10]
    
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            metadatas=[{"source": "cv"}],
            ids=[f"cv_chunk_{i}"]
        )
    
    print(f"Successfully indexed {len(chunks)} chunks in Python 3.11!")

if __name__ == "__main__":
    reset_and_chunk_cv()