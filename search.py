from pathlib import Path
from langchain_qdrant import QdrantVectorStore
from embeddings import get_embeddings

DB_PATH = Path(__file__).parent/"qdrant_db"

store = QdrantVectorStore.from_existing_collection(
    embedding=get_embeddings(),
    path= str(DB_PATH),
    collection_name="stvo"
)

questions = [
    "wer hat an einer kreuzung ohne verkehrszeichen vorfahrt?",
    "who has right of way at a crossing without traffic signs"
]

for q in questions:
    print("="*60)
    print("Q:",q)
    for doc, score in store.similarity_search_with_score(q,k=3):
        print(f"\n [Score {score:.3f}] page {doc.metadata['page']}")
        print(doc.page_content[:300])

store.client.close()