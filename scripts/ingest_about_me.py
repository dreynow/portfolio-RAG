import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.database import collection

def ingest_about_me():
    md_path = "data/processed/about-me.md"

    if not os.path.exists(md_path):
        print(f"Error: File not found at {md_path}")
        return

    with open(md_path, "r") as f:
        content = f.read()

    # Split by section headers (##) to create meaningful chunks
    sections = content.split("\n## ")
    chunks = []

    # First chunk is the intro (before first ##)
    if sections[0].strip():
        chunks.append(sections[0].strip())

    # Remaining chunks include their headers
    for section in sections[1:]:
        chunk = "## " + section.strip()
        if len(chunk) > 30:
            chunks.append(chunk)

    # Remove existing about-me chunks (if re-running)
    existing = collection.get()
    about_me_ids = [id for id in existing['ids'] if id.startswith("about_me_")]
    if about_me_ids:
        collection.delete(ids=about_me_ids)
        print(f"Removed {len(about_me_ids)} old about-me chunks.")

    # Add new chunks
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            metadatas=[{"source": "about_me_md"}],
            ids=[f"about_me_chunk_{i}"]
        )

    print(f"Success! Indexed {len(chunks)} chunks from about-me.md")

if __name__ == "__main__":
    ingest_about_me()
