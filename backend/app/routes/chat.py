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
        chunks = retrieve_chunks(request.query, top_k=5)  # Increased from 3 to 5
        if not chunks:
            raise HTTPException(status_code=404, detail="No relevant HVAC documents found. The knowledge base may be empty or experiencing issues.")

        # Improved context building with better formatting
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            text = chunk.get("text", "").strip()
            if text:
                context_parts.append(f"Source {i}: {text}")
        
        context = "\n\n".join(context_parts)
        
        # Better prompt engineering
        prompt = f"""Based on the following HVAC documentation context, provide a comprehensive and accurate answer to the question.

Context:
{context}

Question: {request.query}

Please provide a detailed answer based on the context above. If the context doesn't contain enough information, mention what additional information might be needed.

Answer:"""

        answer = generate_answer(prompt)

        # Build sources safely with improved logic
        sources: List[Source] = []
        for c in chunks:
            text = c.get("text", "")
            if not text:
                continue
            
            # Include sources even without URLs for completeness
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