from pathlib import Path
from langchain_qdrant import QdrantVectorStore
from ingest import load_chunks_by_paragraph
from embeddings import get_embeddings

DB_PATH = Path(__file__).parent/"qdrant_db"

chunks = load_chunks_by_paragraph()
print(f"Embedding {len(chunks)} chunks ")
QdrantVectorStore.from_documents(
    chunks,
    get_embeddings(),
    path=str(DB_PATH),
    collection_name="stvo",
    force_recreate=True)
print("Indext built in ",DB_PATH)