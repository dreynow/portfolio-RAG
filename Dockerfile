FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for llama.cpp
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY scripts/ scripts/
COPY prompts/ prompts/
COPY frontend/ frontend/
COPY data/ data/
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

EXPOSE 5001

ENTRYPOINT ["./entrypoint.sh"]
