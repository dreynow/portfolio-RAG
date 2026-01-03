import os
import re
import pymupdf4llm
from scripts.database import collection

def smart_chunk_cv(md_text):
    """
    Chunks CV by keeping job entries together (date + company + bullets).
    Also preserves other sections like skills, education, etc.
    """
    lines = md_text.split('\n')
    chunks = []
    current_chunk = []

    # Pattern to detect job entry starts (date ranges like "Feb. 2024 - Present")
    date_pattern = re.compile(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\.?\s+\d{4}', re.IGNORECASE)

    # Pattern to detect section headers
    section_pattern = re.compile(r'^\*\*(Objective|Job Experience|Education|Skills|Papers|Referees|Certifications)', re.IGNORECASE)

    for line in lines:
        stripped = line.strip()

        # Check if this line starts a new job entry or section
        is_new_job = date_pattern.match(stripped)
        is_new_section = section_pattern.match(stripped)

        if (is_new_job or is_new_section) and current_chunk:
            # Save previous chunk
            chunk_text = '\n'.join(current_chunk).strip()
            if len(chunk_text) > 30:
                chunks.append(chunk_text)
            current_chunk = []

        if stripped:  # Skip empty lines but keep content
            current_chunk.append(line)

    # Don't forget the last chunk
    if current_chunk:
        chunk_text = '\n'.join(current_chunk).strip()
        if len(chunk_text) > 30:
            chunks.append(chunk_text)

    return chunks

def ingest_pdf_cv():
    pdf_path = "data/raw/cv.pdf"

    if not os.path.exists(pdf_path):
        print(f"Error: Put your CV PDF at {pdf_path}")
        return

    # 1. Convert PDF to Markdown
    print("Converting PDF to searchable text...")
    md_text = pymupdf4llm.to_markdown(pdf_path)

    # 2. Smart chunking - keeps job entries together
    chunks = smart_chunk_cv(md_text)

    # 3. Clear only old CV chunks (preserve about-me chunks)
    existing = collection.get()
    cv_ids = [id for id in existing['ids'] if id.startswith('cv_chunk_')]
    if cv_ids:
        collection.delete(ids=cv_ids)
        print(f"Removed {len(cv_ids)} old CV chunks.")

    # 4. Add new chunks
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            metadatas=[{"source": "cv_pdf"}],
            ids=[f"cv_chunk_{i}"]
        )
    print(f"Success! Indexed {len(chunks)} chunks of experience.")

if __name__ == "__main__":
    ingest_pdf_cv()