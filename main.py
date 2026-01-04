# /// script
# dependencies = [
#     "fastapi",
#     "uvicorn",
#     "pydantic-settings",
#     "openai",
#     "chromadb",
#     "sentence-transformers",
# ]
# ///
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from scripts.query import stream_portfolio_assistant
import os

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def read_root():
    return FileResponse('frontend/index.html')

class ChatRequest(BaseModel):
    question: str

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(
        stream_portfolio_assistant(request.question), 
        media_type="text/plain"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)