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
    try:
        chunks = retrieve_chunks(request.query, top_k=3)  # 3 for token limits
        if not chunks:
            raise HTTPException(status_code=404, detail="No relevant HVAC documents found. The knowledge base may be empty or experiencing issues.")

        # Build context with length control
        context_parts = []
        total_chars = 0
        max_context_chars = 1200  # Roughly 300 tokens for context
        
        for i, chunk in enumerate(chunks, 1):
            text = chunk.get("text", "").strip()
            if text and total_chars < max_context_chars:
                # Truncate individual chunk if too long
                if len(text) > 400:
                    text = text[:400] + "..."
                
                chunk_text = f"Source {i}: {text}"
                if total_chars + len(chunk_text) <= max_context_chars:
                    context_parts.append(chunk_text)
                    total_chars += len(chunk_text)
                else:
                    # Add partial chunk if there's still room
                    remaining = max_context_chars - total_chars
                    if remaining > 50:
                        context_parts.append(chunk_text[:remaining-3] + "...")
                    break
        
        context = "\n\n".join(context_parts)
        
        # Concise prompt to stay within token limits
        prompt = f"""Context: {context}

Question: {request.query}

Answer based on the context:"""

        answer = generate_answer(prompt)

        # Only build sources if the answer actually uses documentation
        # Check if answer mentions documentation or contains technical HVAC content
        uses_docs = any(phrase in answer.lower() for phrase in [
            "documentation", "from the hvac", "according to", "based on the hvac",
            "from the documentation"
        ])
        
        sources: List[Source] = []
        if uses_docs and chunks:
            for c in chunks:
                text = c.get("text", "")
                if not text:
                    continue
                
                # Include sources only when documentation is actually referenced
                raw_url = c.get("url") or None
                snippet = (text[:200] + "…").replace("\n", " ") if len(text) > 200 else text
                
                sources.append(Source(
                    title=c.get("title", "HVAC Document"),
                    url=raw_url,
                    chunk_id=c.get("chunk_id", 0) + 1,
                    snippet=snippet,
                ))
            
        return ChatResponse(answer=answer, sources=sources)
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your HVAC query. Please try again.")