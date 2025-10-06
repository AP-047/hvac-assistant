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
from qdrant_client.http.exceptions import ResponseHandlingException, UnexpectedResponse
import uuid

PDF_SOURCES = [
    {
        "title": "NASA Goddard Space Flight Center Cleanroom Filtration and HVAC Designs (2024)",
        "url":   "https://ntrs.nasa.gov/api/citations/20240010626/downloads/ASHRAE%20CEIC%20Presentation_Rev0.pdf",
        "path":  "docs/sources/NASA_Goddard_Space_Flight_Center_Cleanroom_Filtration_&_HVAC_Designs_(2024).pdf",
    },
    {
        "title": "Operations Support Building HVAC Analysis (1986)",
        "url":   "https://ntrs.nasa.gov/api/citations/19860018818/downloads/19860018818.pdf",
        "path":  "docs/sources/Operations_Support_Building_HVAC_Analysis_(1986).pdf",
    },
    {
        "title": "Residential Heating & Cooling System (1972)",
        "url":   "https://ntrs.nasa.gov/api/citations/19730009184/downloads/19730009184.pdf",
        "path":  "docs/sources/Residential_Heating_&_Cooling_System_(1972).pdf",
    },
    {
        "title": "Air Conditioning System & Component (1974)",
        "url":   "https://ntrs.nasa.gov/api/citations/19740019789/downloads/19740019789.pdf",
        "path":  "docs/sources/Air_Conditioning_System_&_Component_(1974).pdf",
    },
    {
        "title": "Solar-Powered Residential Air Conditioner (1975)",
        "url":   "https://ntrs.nasa.gov/api/citations/19760013544/downloads/19760013544.pdf",
        "path":  "docs/sources/Solar-Powered_Residential_Air_Conditioner_(1975).pdf",
    },
    {
        "title": "HVAC Functional Inspection & Testing Guide (NIST)",
        "url":   "https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir4758.pdf",
        "path":  "docs/sources/HVAC_Functional_Inspection_&_Testing_Guide_(NIST).pdf",
    },
    {
        "title": "VA HVAC Design Manual (2024)",
        "url":   "https://www.cfm.va.gov/til/dmanual/dmHVAC.pdf",
        "path":  "docs/sources/VA_HVAC_Design_Manual_(2024).pdf",
    },
    {
        "title": "NSPIRE Standard – HVAC (HUD, 2021)",
        "url":   "https://www.hud.gov/sites/dfiles/PIH/documents/NSPIRE-Standards-v2.1-HVAC.pdf",
        "path":  "docs/sources/NSPIRE_Standard–HVAC_(HUD,2021).pdf",
    },
    {
        "title": "UFC 3-410-01 HVAC Criteria (2013)",
        "url":   "https://www.wbdg.org/FFC/DOD/UFC/ufc_3_410_01_2013_c9.pdf",
        "path":  "docs/sources/UFC_3-410-01_HVAC_Criteria_(2013).pdf",
    },
    {
        "title": "EMU HVAC Standards (2008)",
        "url":   "https://www.emich.edu/physical-plant/documents/construction-standards/division-23-heating-ventilation-and-air-conditioning.pdf",
        "path":  "docs/sources/EMU_HVAC_Standards_(2008).pdf",
    },
    {
        "title": "EU Ecodesign Guidelines for HVAC",
        "url":   "https://energy-efficient-products.ec.europa.eu/document/download/70f79d6b-75c7-4804-b3a0-f8d187a87a70_en",
        "path":  "docs/sources/EU_Ecodesign_HVAC.pdf",
    },
]

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

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """Split text into overlapping chunks for better context preservation"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        if chunk.strip():  # Only add non-empty chunks
            chunks.append(chunk)
        # Break if we've reached the end
        if i + chunk_size >= len(words):
            break
    return chunks


def check_qdrant_health():
    """Check if Qdrant is healthy and accessible"""
    try:
        collections = client.get_collections()
        print(f"Qdrant is healthy. Collections: {[c.name for c in collections.collections]}")
        return True
    except Exception as e:
        print(f"Qdrant health check failed: {e}")
        return False

def create_collection_if_not_exists():
    """Ensure Qdrant collection exists with robust error handling"""
    try:
        # Check if collection exists by trying to count vectors
        count = client.count(collection_name=COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' already exists with {count.count} vectors")
        return True
    except Exception as e:
        print(f"Collection doesn't exist or needs recreation: {e}")
        
    # Try to delete collection if it exists but is corrupted
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted existing collection '{COLLECTION_NAME}'")
    except Exception:
        print(f"No existing collection to delete")
        
    # Create fresh collection
    try:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        print(f"Successfully created collection '{COLLECTION_NAME}'")
        return True
    except Exception as e:
        print(f"Failed to create collection: {e}")
        return False

def ingest_documents(source_dir: str):
    """Ingest new or modified documents"""
    # Check Qdrant health first
    if not check_qdrant_health():
        print("Qdrant is not healthy. Exiting.")
        return
        
    if not create_collection_if_not_exists():
        print("Failed to create/verify collection. Exiting.")
        return
    
    # Load existing metadata
    metadata = load_metadata()
    new_metadata = {}
    
    # Loop over the predefined PDF_SOURCES
    for src in PDF_SOURCES:
        pdf_path = Path(src["path"])
        filename = pdf_path.name
        file_hash = get_file_hash(pdf_path)

        # Skip unchanged files (as before)...
        if filename in metadata and metadata[filename] == file_hash:
            print(f"Skipping {filename} (unchanged)")
            new_metadata[filename] = file_hash
            continue

        print(f"Processing {filename}...")
        # Extract text
        reader = PdfReader(str(pdf_path))
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

        # Chunk text
        chunks = chunk_text(full_text)
        print(f"  Created {len(chunks)} chunks")

        # Build points with enriched payload
        points = []
        for idx, chunk in enumerate(chunks):
            if chunk.strip():
                vector = embedder.encode(chunk).tolist()
                point_id = str(uuid.uuid4())
                points.append({
                    "id": point_id,
                    "vector": vector,
                    "payload": {
                        "text":     chunk,
                        "title":    src["title"],
                        "url":      src["url"],
                        "chunk_id": idx,
                        "file_hash": file_hash
                    }
                })

        # Upsert to Qdrant
        if points:
            client.upsert(collection_name=COLLECTION_NAME, points=points)
            print(f"  Ingested {len(points)} chunks from {filename}")
            new_metadata[filename] = file_hash
        else:
            print(f"Warning: No valid chunks created from {filename}")

    
    # Save updated metadata
    save_metadata(new_metadata)
    print(f"\nIngestion complete! Processed {len([f for f in new_metadata if f not in metadata])} new/modified files")

if __name__ == "__main__":
    ingest_documents("/app/docs/sources")