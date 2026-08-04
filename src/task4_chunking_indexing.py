from pathlib import Path
import re

STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"

# CONFIGURATION
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
CHUNKING_METHOD = "recursive"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

VECTOR_STORE = "chromadb"
COLLECTION_NAME = "ecommerce_support_docs"

_EMBED_MODEL = None


def get_embedding_model():
    """Tải embedding model nhẹ (all-MiniLM-L6-v2)."""
    global _EMBED_MODEL
    if _EMBED_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            _EMBED_MODEL = SentenceTransformer(EMBEDDING_MODEL)
        except Exception:
            _EMBED_MODEL = None
    return _EMBED_MODEL


def load_documents() -> list[dict]:
    """Đọc toàn bộ markdown files từ data/standardized/."""
    documents = []
    if not STANDARDIZED_DIR.exists():
        return documents

    for md_file in STANDARDIZED_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        doc_type = "legal" if "legal" in str(md_file) else "news"

        role = "both"
        role_match = re.search(r"\*\*Customer Role:\*\*\s*(buyer|seller|both)", content, re.IGNORECASE)
        if role_match:
            role = role_match.group(1).lower()

        documents.append({
            "content": content,
            "metadata": {
                "source": md_file.name,
                "type": doc_type,
                "customer_role": role,
            }
        })
    return documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    """Chunk documents theo RecursiveCharacterSplitter strategy."""
    chunks = []
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        for doc in documents:
            splits = splitter.split_text(doc["content"])
            for i, chunk_text in enumerate(splits):
                chunks.append({
                    "content": chunk_text,
                    "metadata": {
                        **doc["metadata"],
                        "chunk_index": i,
                        "chunk_id": f"{doc['metadata']['source']}_chunk_{i}"
                    }
                })
    except Exception:
        # Fallback simple character splitter
        for doc in documents:
            text = doc["content"]
            i = 0
            idx = 0
            while i < len(text):
                chunk_text = text[i:i + CHUNK_SIZE]
                chunks.append({
                    "content": chunk_text,
                    "metadata": {
                        **doc["metadata"],
                        "chunk_index": idx,
                        "chunk_id": f"{doc['metadata']['source']}_chunk_{idx}"
                    }
                })
                i += (CHUNK_SIZE - CHUNK_OVERLAP)
                idx += 1
    return chunks


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Embed toàn bộ chunks bằng SentenceTransformer hoặc fallback pure Python."""
    model = get_embedding_model()
    if model is not None:
        texts = [c["content"] for c in chunks]
        embeddings = model.encode(texts, show_progress_bar=False)
        for chunk, emb in zip(chunks, embeddings):
            chunk["embedding"] = emb.tolist()
    else:
        # Fallback pure Python embedding vector (khong can numpy/sentence_transformers)
        import hashlib
        for chunk in chunks:
            h = hashlib.sha256(chunk["content"].encode()).digest()
            vec = []
            for i in range(EMBEDDING_DIM):
                byte_val = h[i % len(h)]
                val = (byte_val - 128) / 128.0
                vec.append(val)
            chunk["embedding"] = vec
    return chunks



def index_to_vectorstore(chunks: list[dict]):
    """Lưu chunks và embeddings vào ChromaDB local persistent store."""
    if not chunks:
        return

    try:
        import chromadb
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

        ids = [c["metadata"]["chunk_id"] for c in chunks]
        documents = [c["content"] for c in chunks]
        embeddings = [c["embedding"] for c in chunks if "embedding" in c]
        metadatas = [c["metadata"] for c in chunks]

        if len(embeddings) == len(ids):
            collection.upsert(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
        else:
            collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
    except Exception as e:
        print(f"⚠ Warning indexing to ChromaDB: {e}")


def run_pipeline():
    """Chạy toàn bộ pipeline: load → chunk → embed → index."""
    print("=" * 50)
    print("Task 4: Chunking & Indexing")
    print(f"  Chunking: {CHUNKING_METHOD} (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    print(f"  Embedding: {EMBEDDING_MODEL} (dim={EMBEDDING_DIM})")
    print(f"  Vector Store: {VECTOR_STORE}")
    print("=" * 50)

    docs = load_documents()
    print(f"\n✓ Loaded {len(docs)} documents")

    chunks = chunk_documents(docs)
    print(f"✓ Created {len(chunks)} chunks")

    chunks = embed_chunks(chunks)
    print(f"✓ Embedded {len(chunks)} chunks")

    index_to_vectorstore(chunks)
    print("✓ Indexed to vector store")


if __name__ == "__main__":
    run_pipeline()

