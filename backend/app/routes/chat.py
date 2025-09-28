from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.services.retrieval import retrieve_chunks
from app.services.llm import generate_answer

router = APIRouter()

class Source(BaseModel):
    title:    str
    url:      HttpUrl
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
        raise HTTPException(status_code=404, detail="No relevant documents found")

    # Build prompt context from full chunk text
    context = "\n\n".join(c["text"] for c in chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {request.query}\nAnswer:"
    answer = generate_answer(prompt)

    # Build rich source objects with snippet previews
    sources = [
        Source(
            title=c["title"],
            url=c["url"],
            chunk_id=c["chunk_id"] + 1,
            snippet=(c["text"][:200] + "…").replace("\n", " ")
        )
        for c in chunks
    ]

    return ChatResponse(answer=answer, sources=sources)