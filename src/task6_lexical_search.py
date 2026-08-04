"""
Task 6 — Lexical Search Module (BM25).

Mặc định sử dụng BM25. Nếu dùng phương pháp khác (TF-IDF, Elasticsearch,
Weaviate BM25 built-in), hãy giải thích cơ chế trong buổi demo → +5 bonus.

Cài đặt:
    pip install rank-bm25

BM25 hoạt động thế nào:
    - Term Frequency (TF): từ xuất hiện nhiều trong document → điểm cao
    - Inverse Document Frequency (IDF): từ hiếm → quan trọng hơn
    - Document length normalization: document dài không bị ưu tiên quá mức
    - Formula: score(q,d) = Σ IDF(qi) * (tf(qi,d) * (k1+1)) / (tf(qi,d) + k1*(1-b+b*|d|/avgdl))
    - k1=1.5 (term saturation), b=0.75 (length normalization)
"""

import re
from pathlib import Path

CORPUS: list[dict] = []
_BM25_INDEX = None


def get_corpus() -> list[dict]:
    """Tải và cache corpus từ task4 chunk_documents."""
    global CORPUS
    if not CORPUS:
        try:
            from src.task4_chunking_indexing import load_documents, chunk_documents
            docs = load_documents()
            CORPUS = chunk_documents(docs)
        except Exception:
            CORPUS = []
    return CORPUS


def _tokenize(text: str) -> list[str]:
    """Tokenize đơn giản tách theo từ và loại bỏ ký tự đặc biệt."""
    return re.findall(r"\w+", text.lower())


def build_bm25_index(corpus: list[dict]):
    """Xây dựng BM25 index từ corpus."""
    global _BM25_INDEX
    if not corpus:
        return None

    try:
        from rank_bm25 import BM25Okapi
        tokenized_corpus = [_tokenize(doc["content"]) for doc in corpus]
        _BM25_INDEX = BM25Okapi(tokenized_corpus)
        return _BM25_INDEX
    except Exception:
        _BM25_INDEX = None
        return None


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """Tìm kiếm từ khóa sử dụng BM25 (hoặc TF-IDF / term overlap fallback)."""
    corpus = get_corpus()
    if not corpus:
        return []

    global _BM25_INDEX
    if _BM25_INDEX is None:
        build_bm25_index(corpus)

    tokenized_query = _tokenize(query)

    if _BM25_INDEX is not None:
        scores = _BM25_INDEX.get_scores(tokenized_query)
        results = []
        for idx, score in enumerate(scores):
            results.append({
                "content": corpus[idx]["content"],
                "score": round(float(score), 4),
                "metadata": corpus[idx]["metadata"]
            })
    else:
        # Fallback term frequency score
        query_set = set(tokenized_query)
        results = []
        for doc in corpus:
            tokens = _tokenize(doc["content"])
            match_count = sum(1 for t in tokens if t in query_set)
            score = match_count / max(1, len(tokens) ** 0.5)
            results.append({
                "content": doc["content"],
                "score": round(score, 4),
                "metadata": doc["metadata"]
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    results = lexical_search("phương thức thanh toán shopee", top_k=5)
    for r in results:
        print(f"[{r['score']:.3f}] {r['content'][:100]}...")

