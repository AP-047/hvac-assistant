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

def check_collection_health() -> bool:
    """Check if the collection exists and is accessible"""
    try:
        # Skip get_collection() due to schema compatibility issues
        # Just check if we can count vectors - this is sufficient
        count = client.count(collection_name=COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' has {count.count} vectors")
        return count.count > 0
    except Exception as e:
        print(f"Collection health check failed: {e}")
        return False

def retrieve_chunks(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Embed the query, search Qdrant for the most similar document chunks,
    and return their payloads including text, title, URL, and chunk_id.
    """
    try:
        # Check if collection is healthy before proceeding
        if not check_collection_health():
            print(f"Collection '{COLLECTION_NAME}' is not available or empty")
            return []

        # 1. Embed user query
        query_vector = embedder.encode(query).tolist()

        # 2. Search the collection
        search_result = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True,
        )

        if not search_result:
            print("No search results found")
            return []

        # 3. Extract and return rich payloads
        sources = []
        for hit in search_result:
            if hit.payload:
                payload = hit.payload
                sources.append({
                    "text":     payload.get("text", ""),
                    "title":    payload.get("title", "Unknown Document"),
                    "url":      payload.get("url", ""),
                    "chunk_id": payload.get("chunk_id", 0),
                    "score":    hit.score,  # Add relevance score
                })
        
        print(f"Retrieved {len(sources)} chunks for query: {query[:50]}...")
        return sources
        
    except Exception as e:
        print(f"Retrieval error: {e}")
        return []