import os
import time
import requests
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Environment and constants
QDRANT_URL = os.getenv("QDRANT_URL", "https://hvac-qdrant.azurewebsites.net")
COLLECTION_NAME = "hvac_docs"

# Initialize embedder once
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def get_qdrant_client():
    """Create a new Qdrant client with conservative settings"""
    return QdrantClient(
        url=QDRANT_URL, 
        timeout=60,  # Reduced timeout for faster failure
        prefer_grpc=False  # Use HTTP instead of gRPC for better Azure compatibility
    )

def check_collection_health() -> bool:
    """Check if the collection exists and is accessible using HTTP only (faster)"""
    try:
        print("Checking collection health via HTTP...")
        response = requests.get(f'{QDRANT_URL}/collections/{COLLECTION_NAME}', timeout=15)
        if response.status_code == 200:
            data = response.json()
            points_count = data.get('result', {}).get('points_count', 0)
            print(f"Collection '{COLLECTION_NAME}' has {points_count} vectors")
            return points_count > 0
        else:
            print(f"HTTP health check failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"HTTP health check failed: {e}")
        return False

def is_hvac_related(query: str) -> bool:
    """Check if the query is related to HVAC topics"""
    hvac_keywords = [
        'hvac', 'heating', 'ventilation', 'air conditioning', 'cooling', 'temperature control',
        'thermostat', 'furnace', 'boiler', 'heat pump', 'ductwork', 'filter', 
        'compressor', 'condenser', 'evaporator', 'refrigeration', 'chiller',
        'air quality', 'humidity', 'ventilator', 'fan', 'blower', 'damper',
        'coil', 'vav', 'rtu', 'unit heater', 'radiant', 'geothermal',
        'climate control', 'indoor air', 'system design', 'energy efficiency'
    ]
    
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in hvac_keywords)

def retrieve_chunks(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Embed the query, search Qdrant for the most similar document chunks,
    and return their payloads including text, title, URL, and chunk_id.
    Only searches if query is HVAC-related.
    """
    try:
        # First check if query is HVAC-related
        if not is_hvac_related(query):
            print(f"Query '{query}' is not HVAC-related, skipping retrieval")
            return []
            
        # Check if collection is healthy before proceeding
        if not check_collection_health():
            print(f"Collection '{COLLECTION_NAME}' is not available or empty")
            return []

        # 1. Embed user query
        query_vector = embedder.encode(query).tolist()

        # 2. Use HTTP search directly (faster and more reliable)
        print("Searching via HTTP API...")
        
        # 3. HTTP search
        try:
            print("Trying HTTP fallback for search...")
            search_payload = {
                "vector": query_vector,
                "limit": top_k,
                "with_payload": True
            }
            
            response = requests.post(
                f'{QDRANT_URL}/collections/{COLLECTION_NAME}/points/search',
                json=search_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                search_results = data.get('result', [])
                
                sources = []
                for hit in search_results:
                    payload = hit.get('payload', {})
                    sources.append({
                        "text":     payload.get("text", ""),
                        "title":    payload.get("title", "Unknown Document"),
                        "url":      payload.get("url", ""),
                        "chunk_id": payload.get("chunk_id", 0),
                        "score":    hit.get('score', 0.0),
                    })
                
                print(f"HTTP search retrieved {len(sources)} chunks")
                return sources
            else:
                print(f"HTTP search failed with status: {response.status_code}")
                
        except Exception as e:
            print(f"HTTP search failed: {e}")
            
        return []
        
    except Exception as e:
        print(f"Retrieval error: {e}")
        return []