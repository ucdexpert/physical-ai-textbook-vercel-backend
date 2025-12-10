
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List
import os

# Import with error handling
try:
    from agent import textbook_agent
    from agents.run import Runner
    AGENT_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import agent: {e}")
    AGENT_AVAILABLE = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Physical AI RAG API...")
    print(f"Agent available: {AGENT_AVAILABLE}")
    yield
    # Shutdown
    print("Shutting down Physical AI RAG API...")

app = FastAPI(title="Physical AI RAG API", lifespan=lifespan)

# ✅ CORS - Sirf FRONTEND URLs
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://physical-ai-textbook-frontend.vercel.app",  # ✅ Frontend URL
    "https://physical-ai-textbook-frontend-*.vercel.app",  # ✅ Preview deployments
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

# ✅ Root endpoint for Vercel
@app.get("/")
async def root():
    """Root endpoint for Vercel health check"""
    return {
        "status": "ok",
        "service": "Physical AI RAG API",
        "agent_available": AGENT_AVAILABLE
    }

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "Physical AI Agent",
        "agent_available": AGENT_AVAILABLE
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # ✅ Check agent availability first
    if not AGENT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Agent is not available. Check server logs."
        )
    
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        print(f"Processing query: {request.query}")
        response = await Runner.run(textbook_agent, request.query)
        print("Agent execution finished")

        # Convert the agent response to text
        if hasattr(response, "final_output"):
            final_answer = response.final_output
        else:
            final_answer = str(response)

        return ChatResponse(answer=final_answer)

    except Exception as e:
        error_msg = str(e)
        print("Agent Error:", error_msg)
        
        if "429" in error_msg or "Resource exhausted" in error_msg:
             raise HTTPException(
                 status_code=429,
                 detail="Rate limit exceeded. Please try again later."
             )
             
        raise HTTPException(status_code=500, detail=error_msg)

# ✅ Vercel handler - CRITICAL!
handler = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)



