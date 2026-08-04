# Bài Tập Nhóm — E-commerce Support RAG Chatbot

## Mục Tiêu

Sau khi hoàn thành bài cá nhân, nhóm ngồi lại để xây dựng **1 trong 2 sản phẩm**:

---

## Yêu cầu 1: Sản phẩm nhóm RAG Chatbot

Xây dựng chatbot trả lời câu hỏi về chính sách thương mại điện tử và hỗ trợ khách hàng liên quan.

**Yêu cầu:**
- Giao diện chat (Streamlit / Gradio / Chainlit)
- Trả lời có citation (dựa trên Task 10)
- Hỗ trợ follow-up questions (conversation memory)
- Hiển thị source documents đã dùng

**Stack gợi ý:**
```
Chainlit/Streamlit → Retrieval (Task 9) → Generation (Task 10) → Display
```

---

## Yêu cầu 2: RAG Evaluation Pipeline

Sử dụng **1 trong 3 framework** sau để evaluate pipeline RAG của nhóm:

### Framework lựa chọn

| Framework | Cài đặt | Đặc điểm |
|-----------|---------|-----------|
| [DeepEval](https://github.com/confident-ai/deepeval) | `pip install deepeval` | Nhiều metric built-in, dễ integrate với pytest |
| [RAGAS](https://github.com/explodinggradients/ragas) | `pip install ragas` | Chuẩn industry cho RAG eval, 3 trục chính |
| [TruLens](https://github.com/truera/trulens) | `pip install trulens` | Dashboard UI, feedback functions mạnh |

### Yêu cầu Evaluation

1. **Tạo Golden Dataset** — tối thiểu 15 cặp Q&A (question, expected_answer, expected_context)
2. **Chạy evaluation** trên toàn bộ golden dataset với các metrics sau:
   - **Faithfulness** — câu trả lời có bám đúng context không?
   - **Answer Relevance** — câu trả lời có đúng câu hỏi không?
   - **Context Recall** — retriever có lấy đủ evidence không?
   - **Context Precision** — trong context lấy về, bao nhiêu % thực sự hữu ích?
3. **So sánh A/B** — chạy eval trên ít nhất 2 config khác nhau (ví dụ: có reranking vs không reranking, hoặc hybrid vs dense-only)
4. **Báo cáo** — bảng điểm + phân tích worst performers + đề xuất cải tiến

Xem code mẫu (DeepEval/RAGAS/TruLens) chi tiết trong `README.md` gốc mục "Yêu cầu 2".

### Deliverable Evaluation

- [ ] File `group_project/evaluation/golden_dataset.json` — 15+ cặp Q&A
- [ ] File `group_project/evaluation/eval_pipeline.py` — script chạy evaluation
- [ ] File `group_project/evaluation/results.md` — bảng điểm + phân tích
- [ ] So sánh A/B ít nhất 2 configs

---

## Yêu Cầu Chung

1. **Tích hợp pipeline** từ bài cá nhân của các thành viên
2. **Demo hoạt động được** trong buổi trình bày (chạy local hoặc deploy)
3. **Evaluation pipeline** chạy được và có báo cáo kết quả
4. **Code push lên repository** chung của nhóm
5. **README** mô tả kiến trúc và phân công (điền bên dưới)

---

## Kiến Trúc Hệ Thống

```
User Query
    │
    ▼
┌──────────────────────────────────────────────────────────┐
│                   Hybrid Search Engine                   │
│   ┌────────────────────────┐   ┌─────────────────────┐   │
│   │ Dense Retrieval        │   │ Sparse Retrieval    │   │
│   │ (ChromaDB + Cosine)    │   │ (BM25Okapi Keyword) │   │
│   └───────────┬────────────┘   └──────────┬──────────┘   │
└───────────────┼───────────────────────────┼──────────────┘
                └─────────────┬─────────────┘
                              ▼
┌──────────────────────────────────────────────────────────┐
│                 RRF Reranking (k = 60)                   │
└─────────────────────────────┬────────────────────────────┘
                              ▼
               [Cosine Score < 0.48 Threshold?]
               ├── Yes ──► PageIndex Vectorless Fallback
               └── No  ──► Top-K Chunks
                              │
                              ▼
┌──────────────────────────────────────────────────────────┐
│                Document Reordering (Task 10)             │
│            Mitigating "Lost in the Middle" Effect        │
└─────────────────────────────┬────────────────────────────┘
                              ▼
┌──────────────────────────────────────────────────────────┐
│                LLM Generation (Citation)                 │
└──────────────────────────────────────────────────────────┘
```

---

## Phân Công Công Việc

| Thành viên | Vị trí / Role | Nhiệm vụ đảm nhận | Trạng thái |
|---|---|---|:---:|
| **Kiều Hồng Phong** | Leader & RAG Architect | Quản lý pipeline chính (`task9`), Reordering & Chatbot UI | ✅ Hoàn thành |
| **Lê Mai Việt Hoàng** | Dense & Vector Specialist | Chunking & Indexing ChromaDB (`task4`), Semantic Search (`task5`) | ✅ Hoàn thành |
| **Đỗ Duy Đức** | Data Engineering Specialist | Thu thập chính sách (`task1`), convert Markdown (`task3`) | ✅ Hoàn thành |
| **Nguyễn Đức Đạt** | Sparse & Reranking Specialist | BM25 Lexical Search (`task6`), RRF Reranking (`task7`) | ✅ Hoàn thành |
| **Vũ Nguyễn Bảo Sơn** | Evaluation & QA Specialist | Fallback PageIndex (`task8`), RAGAS Evaluation Benchmark (`eval_pipeline`) | ✅ Hoàn thành |

---

## Hướng Dẫn Chạy Dự Án

### 1. Chuẩn bị Môi trường & Khởi tạo Vector DB
```powershell
# Chạy chuyển đổi dữ liệu thô sang Markdown
uv run python -m src.task3_convert_markdown

# Cắt đoạn (Chunking) và nạp dữ liệu vào ChromaDB
uv run python -X utf8 src/task4_chunking_indexing.py
```

### 2. Chạy Ứng Dụng Chatbot (Streamlit UI)
```powershell
uv run streamlit run app.py
```

### 3. Chạy Kiểm Thử Unit Tests (Tất cả 35 Task cá nhân)
```powershell
uv run pytest tests/test_individual.py
```

### 4. Thực Thi RAGAS Evaluation & A/B Benchmark (Bài Nhóm)
```powershell
uv run python -X utf8 -m group_project.evaluation.eval_pipeline
```

---

## Lưu Ý
- Kết quả Đánh giá Benchmark chi tiết được tự động xuất tại: [group_project/evaluation/results.md](file:///d:/AIThucchien/K4-Day08-RAG-Pipeline/group_project/evaluation/results.md)

Hãy giữ lại repo này nếu như bạn học track 3 giai đoạn 2, chúng ta sẽ phát triển tiếp dự án lên knowledge graph để khắc phục các câu hỏi hóc búa khi có các câu hỏi khó.
