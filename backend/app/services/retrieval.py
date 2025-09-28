import os
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Environment and constants
QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
COLLECTION_NAME = "hvac_docs"

# Initialize clients
client = QdrantClient(url=QDRANT_URL)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_chunks(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Embed the query, search Qdrant for the most similar document chunks,
    and return their payloads including text, title, URL, and chunk_id.
    """
    # 1. Embed user query
    query_vector = embedder.encode(query).tolist()

    # 2. Search the collection
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
    )

    # 3. Extract and return rich payloads
    sources = []
    for hit in search_result:
        payload = hit.payload
        sources.append({
            "text":     payload.get("text", ""),
            "title":    payload.get("title", ""),
            "url":      payload.get("url", ""),
            "chunk_id": payload.get("chunk_id", 0),
        })
    return sources