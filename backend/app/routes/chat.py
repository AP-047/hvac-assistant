# backend/app/routes/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.retrieval import retrieve_chunks
from ..services.llm import generate_answer

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    chunks = retrieve_chunks(request.query, top_k=3)
    if not chunks:
        raise HTTPException(status_code=404, detail="No relevant documents found")

    context = "\n".join(chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {request.query}\nAnswer:"

    answer = generate_answer(prompt)
    sources = [f"chunk_{i+1}" for i in range(len(chunks))]
    return ChatResponse(answer=answer, sources=sources)
