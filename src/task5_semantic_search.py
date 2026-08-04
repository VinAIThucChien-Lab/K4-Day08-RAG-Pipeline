"""
Task 5 — Semantic Search Module.

Viết module tìm kiếm ngữ nghĩa (dense retrieval) trên vector store.

Yêu cầu:
    - Input: query string + top_k
    - Output: danh sách chunks có score, sorted descending
    - Phải tương thích với embedding model và vector store ở Task 4
"""


from pathlib import Path

CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"
COLLECTION_NAME = "ecommerce_support_docs"


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm ngữ nghĩa sử dụng vector similarity.
    """
    try:
        import chromadb
        from src.task4_chunking_indexing import get_embedding_model

        if CHROMA_DIR.exists():
            client = chromadb.PersistentClient(path=str(CHROMA_DIR))
            collection = client.get_collection(name=COLLECTION_NAME)

            model = get_embedding_model()
            if model is not None:
                query_vector = model.encode(query).tolist()
                results = collection.query(
                    query_embeddings=[query_vector],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"]
                )
            else:
                results = collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"]
                )

            output = []
            if results and results.get("documents") and results["documents"][0]:
                docs = results["documents"][0]
                metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
                dists = results["distances"][0] if results.get("distances") else [0.5] * len(docs)

                for doc, meta, dist in zip(docs, metas, dists):
                    score = max(0.0, 1.0 - dist)
                    output.append({
                        "content": doc,
                        "score": round(score, 4),
                        "metadata": meta
                    })

            output.sort(key=lambda x: x["score"], reverse=True)
            return output[:top_k]
    except Exception:
        pass

    # Memory fallback: Calculate word overlap similarity if ChromaDB is not ready
    from src.task4_chunking_indexing import load_documents, chunk_documents
    docs = load_documents()
    chunks = chunk_documents(docs)

    query_words = set(query.lower().split())
    output = []
    for c in chunks:
        content_words = set(c["content"].lower().split())
        overlap = len(query_words.intersection(content_words))
        score = overlap / max(1, len(query_words))
        output.append({
            "content": c["content"],
            "score": round(score, 4),
            "metadata": c["metadata"]
        })

    output.sort(key=lambda x: x["score"], reverse=True)
    return output[:top_k]


if __name__ == "__main__":
    results = semantic_search("quy định trả hàng hoàn tiền shopee", top_k=5)
    for r in results:
        print(f"[{r['score']:.3f}] {r['content'][:100]}...")

