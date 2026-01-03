from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from scripts.query import stream_portfolio_assistant

app = FastAPI()

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
    uvicorn.run(app, host="0.0.0.0", port=5000)