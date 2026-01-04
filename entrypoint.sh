#!/bin/bash
set -e

# Initialize ChromaDB if it doesn't exist
if [ ! -d "/app/chroma_db" ] || [ -z "$(ls -A /app/chroma_db 2>/dev/null)" ]; then
    echo "Initializing ChromaDB..."
    python -c "from scripts.ingest_about_me import ingest_about_me; ingest_about_me()"
    echo "ChromaDB initialized."
fi

# Start the application
exec python main.py
