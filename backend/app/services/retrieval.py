import os
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer

QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
COLLECTION_NAME = "hvac_docs"

client = QdrantClient(url=QDRANT_URL)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_chunks(query: str, top_k: int = 5) -> List[str]:
    # 1. Embed the user query
    query_vec = embedder.encode(query).tolist()

    # 2. Perform vector search
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vec,
        limit=top_k,
        with_payload=True
    )

    # 3. Extract chunk texts
    return [hit.payload["text"] for hit in search_result]