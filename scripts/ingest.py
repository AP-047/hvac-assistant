import os
import json
import hashlib
from pathlib import Path
from typing import Dict, Set
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from qdrant_client.http.exceptions import UnexpectedResponse
import uuid

# Load environment
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "hvac_docs"
METADATA_FILE = "ingested_files.json"

# Initialize clients
client = QdrantClient(url=QDRANT_URL)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def get_file_hash(file_path: Path) -> str:
    """Generate hash of file content for change detection"""
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def load_metadata() -> Dict[str, str]:
    """Load metadata of previously ingested files"""
    if Path(METADATA_FILE).exists():
        with open(METADATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_metadata(metadata: Dict[str, str]):
    """Save metadata of ingested files"""
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)

def chunk_text(text: str, max_len: int = 500) -> list:
    """Split text into chunks"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_len):
        chunks.append(" ".join(words[i : i + max_len]))
    return chunks

def create_collection_if_not_exists():
    """Create Qdrant collection if it doesn't exist"""
    try:
        client.get_collection(COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' already exists")
    except UnexpectedResponse:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        print(f"Created collection '{COLLECTION_NAME}'")

def ingest_documents(source_dir: str):
    """Ingest new or modified documents"""
    create_collection_if_not_exists()
    
    # Load existing metadata
    metadata = load_metadata()
    new_metadata = {}
    
    source_path = Path(source_dir)
    pdf_files = list(source_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {source_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF files")
    
    for pdf_path in pdf_files:
        file_hash = get_file_hash(pdf_path)
        filename = pdf_path.name
        
        # Check if file needs processing
        if filename in metadata and metadata[filename] == file_hash:
            print(f"Skipping {filename} (unchanged)")
            new_metadata[filename] = file_hash
            continue
        
        print(f"Processing {filename}...")
        
        try:
            # Extract text from PDF
            reader = PdfReader(str(pdf_path))
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            if not full_text.strip():
                print(f"Warning: No text extracted from {filename}")
                continue
            
            # Chunk and embed
            chunks = chunk_text(full_text)
            print(f"  Created {len(chunks)} chunks")
            
            # Create embeddings and upsert to Qdrant
            points = []
            for idx, chunk in enumerate(chunks):
                if chunk.strip():  # Only process non-empty chunks
                    vector = embedder.encode(chunk).tolist()
                    point_id = str(uuid.uuid4())
                    
                    points.append({
                        "id": point_id,
                        "vector": vector,
                        "payload": {
                            "text": chunk,
                            "source": filename,
                            "chunk_id": idx,
                            "file_hash": file_hash
                        }
                    })
            
            if points:
                # Batch upsert for efficiency
                client.upsert(collection_name=COLLECTION_NAME, points=points)
                print(f"  Ingested {len(points)} chunks from {filename}")
                
                # Update metadata
                new_metadata[filename] = file_hash
            else:
                print(f"Warning: No valid chunks created from {filename}")
                
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            continue
    
    # Save updated metadata
    save_metadata(new_metadata)
    print(f"\nIngestion complete! Processed {len([f for f in new_metadata if f not in metadata])} new/modified files")

if __name__ == "__main__":
    ingest_documents("/app/docs/sources")