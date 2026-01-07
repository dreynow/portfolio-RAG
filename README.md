# Portfolio RAG

A RAG (Retrieval-Augmented Generation) system that answers questions about me using my CV and background information.

## Stack

- **FastAPI** - API server with streaming responses
- **vLLM** - LLM inference server (Qwen2.5-7B-Instruct)
- **ChromaDB** - Vector database for semantic search
- **SentenceTransformers** - Embeddings (all-MiniLM-L6-v2)

## Setup

1. Install dependencies:
```bash
pip install fastapi uvicorn chromadb openai pymupdf4llm sentence-transformers
```

2. Start vLLM server:
```bash
vllm serve Qwen/Qwen2.5-7B-Instruct
```

3. Ingest data:
```bash
python scripts/ingest_cv.py
python scripts/ingest_about_me.py
```

4. Run the API:
```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

## Usage

```bash
curl -X POST http://localhost:5000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"question":"Tell me about yourself"}'
```

## Project Structure

```
├── main.py                 # FastAPI server
├── scripts/
│   ├── database.py         # ChromaDB setup
│   ├── query.py            # RAG pipeline
│   ├── ingest_cv.py        # PDF ingestion
│   └── ingest_about_me.py  # Markdown ingestion
├── prompts/
│   └── system_prompt.txt   # LLM system prompt
└── data/
    ├── raw/                # Source documents (CV PDF)
    └── processed/          # Processed documents (about-me.md)
```
## Deployment

Deployment follows a specific process depending on the type of change. See [.agent/workflows/deploy.md](.agent/workflows/deploy.md) for full details.

### Quick Reference

| Change Type | Location | Deploy Method |
| :--- | :--- | :--- |
| **Python/Frontend code** | `/portfolio/` | Docker build → push → delete pod |
| **K8s deployment config** | `volta/alpha-uno/` | Git push (FluxCD auto-syncs) |
| **vLLM config** | `/portfolio/gpu/` | `sudo systemctl restart vllm` |

For code changes, the standard flow is:
1. `docker build -t dreyybaba/chat:latest .`
2. `docker push dreyybaba/chat:latest`
3. `KUBECONFIG=... kubectl delete pod -n portfolio -l app=portfolio`
