FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY scripts/ scripts/
COPY prompts/ prompts/
COPY frontend/ frontend/
COPY data/ data/

# Copy ChromaDB data if exists
COPY chroma_db/ chroma_db/

EXPOSE 5001

CMD ["python", "main.py"]
