from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import openai  # or your local LLM import
from ..services.llm import retrieve_chunks

router = APIRouter()

openai.api_key = os.getenv("OPENAI_API_KEY")  # if using OpenAI

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Retrieve top chunks
    chunks = retrieve_chunks(request.query, top_k=5)
    if not chunks:
        raise HTTPException(status_code=404, detail="No relevant documents found")

    # Build prompt
    context = "\n\n".join(chunks)
    prompt = (
        f"You are an HVAC design assistant. Use the following context to answer the question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {request.query}\nAnswer:"
    )

    # Call LLM
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=256,
        temperature=0.2,
    )
    answer = response.choices[0].text.strip()

    return ChatResponse(answer=answer, sources=[f"chunk_{i}" for i in range(len(chunks))])