import os
from pathlib import Path
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

# Load environment
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "hvac_docs"

# Initialize clients
client = QdrantClient(url=QDRANT_URL)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, max_len=500):
    words = text.split()
    for i in range(0, len(words), max_len):
        yield " ".join(words[i : i + max_len])

def ingest_documents(source_dir: str):
    # Create collection if not exists
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    # Iterate PDFs
    for pdf_path in Path(source_dir).glob("*.pdf"):
        reader = PdfReader(str(pdf_path))
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() or ""

        # Chunk and embed
        for idx, chunk in enumerate(chunk_text(full_text)):
            vector = embedder.encode(chunk).tolist()
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=[{"id": f"{pdf_path.stem}_{idx}", "vector": vector, "payload": {"text": chunk}}],
            )
        print(f"Ingested {pdf_path.name}")

if __name__ == "__main__":
    ingest_documents("../docs/sources")