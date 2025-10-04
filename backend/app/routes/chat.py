from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from app.services.retrieval import retrieve_chunks
from app.services.llm import generate_answer

router = APIRouter()

class Source(BaseModel):
    title:    str
    url:      Optional[HttpUrl] = None
    chunk_id: int
    snippet:  str

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer:  str
    sources: List[Source]

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    chunks = retrieve_chunks(request.query, top_k=3)
    if not chunks:
        # Provide general answer when documents are unavailable
        prompt = f"Question: {request.query}\nPlease provide a helpful answer about HVAC systems:"
        answer = generate_answer(prompt)
        return ChatResponse(answer=answer, sources=[])

    context = "\n\n".join(c["text"] for c in chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {request.query}\nAnswer:"
    answer = generate_answer(prompt)

    # Build sources safely
    sources: List[Source] = []
    for c in chunks:
        text = c.get("text", "")
        if not text:
            continue
        raw_url = c.get("url") or None     # convert empty string to None
        # Only include entries with a valid URL
        if not raw_url:
            continue
        snippet = (text[:200] + "…").replace("\n", " ")
        sources.append(Source(
            title=c.get("title", "Unknown"),
            url=raw_url,
            chunk_id=c.get("chunk_id", 0) + 1,
            snippet=snippet,
        ))
        
    return ChatResponse(answer=answer, sources=sources)