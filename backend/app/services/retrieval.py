import os
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer

# Environment and constants
QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
COLLECTION_NAME = "hvac_docs"

# Initialize clients
client = QdrantClient(url=QDRANT_URL)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_chunks(query: str, top_k: int = 3) -> List[str]:
    """
    Embed the query, search Qdrant for the most similar document chunks,
    and return their text payloads.
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

    # 3. Extract and return chunk texts
    return [hit.payload["text"] for hit in search_result]
