# CSC4007 — LAB 6: PROMPT ENGINEERING & RETRIEVAL-AUGMENTED GENERATION

**Tên tiếng Việt:** Từ Prompt-only LLM đến RAG Assistant có căn cứ  
**Dữ liệu:** CineSense/IMDB • **Thực hành trên lớp:** 135 phút (3 tiết)  
**Phương án:** Guided scaffold (cấp sẵn chunks, retriever và kiểm tra dữ liệu)  
**Chế độ suy luận:** API, Web UI hoặc sample-output (phải khai báo đúng)  
**Phương thức nộp:** repository GitHub hoặc tệp nén theo hướng dẫn giảng viên.

## 1. Bối cảnh

CineSense từng dùng TF-IDF, RNN/LSTM/GRU và Transformer để phân loại cảm xúc review phim. Nay hệ thống cần giải thích kết quả có căn cứ, và trả lời câu hỏi chỉ dựa trên review packs mà nó được phép truy cập.

Trong lab này, sinh viên phát triển ba phiên bản **liên tục trên cùng nhiệm vụ**:

- **V0 – Baseline Prompt:** một prompt zero-shot có nhiệm vụ và cấu trúc đầu ra rõ ràng.
- **V1 – Improved Prompt:** sau khi phân tích lỗi trên dev, sửa prompt để tăng tính đúng đắn và khả năng kiểm chứng; hai file tương ứng `prompt_v1.txt` và `prompt_v2.txt`.
- **V2 – Single-hop RAG:** lấy ngữ cảnh từ retriever và sinh trả lời kèm ID của chunk hỗ trợ. Có khả năng từ chối khi thiếu bằng chứng.

**Câu hỏi cốt lõi:** Một kết quả nghe hợp lý đã đủ để được coi là đáng tin chưa? Muốn kiểm chứng phải lưu những gì?

**Ngoài phạm vi:** fine-tuning, tự huấn luyện embedding, tự triển khai vector database, multi-hop decomposition, iterative retrieval và agent.

## 2. Mục tiêu thực hành

Sau khi hoàn thành, sinh viên có thể: (i) tạo hai prompt có thay đổi có chủ đích; (ii) ghi nhận đầu ra và đánh giá bằng metric; (iii) phân tích lỗi dựa trên bằng chứng; (iv) sử dụng retriever có sẵn và cấu hình `top_k`; (v) sinh/trình bày câu trả lời có citation, xác định lỗi retrieval và generation; (vi) kiểm thử no-evidence, prompt injection và giới hạn hệ thống.

## 3. Học liệu được cấp

| Thành phần | Mô tả | Trách nhiệm sinh viên |
|---|---|---|
| Review mini-set | 5 dev + 10 eval + 5 stress tùy chọn; nhãn `positive/negative` | Không chỉnh gold labels; chỉ dùng dev để quyết định prompt v2 |
| Knowledge base | 10 review packs, 20 chunks, có `source_file`, `chunk_id` | Kiểm tra nguồn, IDs, ngữ cảnh; không cần tự chunk |
| Retriever | TF-IDF + cosine, truy vấn `top_k` | Thử `k=1` và `k=3`, chọn cấu hình và phân tích |
| QA set | 8 câu có bằng chứng, 2 câu thiếu bằng chứng, 2 câu injection | Kiểm tra retrieval, citation, refusal và bảo vệ chỉ dẫn |
| Sample outputs | Các đầu ra dựng sẵn, tách khỏi live inference | Dùng để thực hành đánh giá, không nói là do mình chạy LLM |

**Nguồn gốc dữ liệu:** Các CSV, review packs và outputs mẫu trong starter kit minh họa là **synthetic teaching examples**. Chúng không phải bản ghi IMDB nguyên bản. Khi giảng viên thay bằng dữ liệu IMDB thật phải công bố dataset/split/nguồn; không trộn dữ liệu mô phỏng với dữ liệu thật trong báo cáo nếu không ghi rõ.

## 4. Quy trình 135 phút

| Chặng | Thời gian | Việc phải làm | Minh chứng chính |
|---|---:|---|---|
| 1. Setup và data check | 15' | Chạy smoke test, kiểm số lượng, đọc metadata, chọn mode | `run_manifest.json`, console log |
| 2. Thiết kế prompt v1/v2 | 35' | Chạy/đọc output dev, nêu tối thiểu 2 lỗi, sửa v2 có giả thuyết | Hai prompt + raw outputs |
| 3. Prompt evaluation | 25' | Khóa prompt, so sánh trên **cùng 10 eval**, tính metric, phân tích 3 lỗi | `prompt_comparison.csv`, `error_analysis.md` |
| 4. Single-hop RAG | 40' | Thử `top_k=1/3`, viết RAG prompt, ghép context và trả lời | `retrieval_top*.csv`, `rag_answers.jsonl` |
| 5. Kiểm chứng | 20' | Citation, no-evidence, injection, phân loại lỗi, chốt báo cáo | `rag_checks.csv`, `lab_report.md` |
| **Tổng** | **135'** | | |

### Chặng 1 – Kiểm tra môi trường và dữ liệu (15 phút)

1. Fork/clone repo, cài `requirements.txt`, chạy `python scripts/smoke_test.py`.
2. Kiểm tra số lượng dev/eval và 3 trường `review_text`, `gold_sentiment`, `source_type`; quan sát ba chunks và `chunk_id` duy nhất.
3. Tạo `run_manifest.json`: nhóm, thời điểm, mode, model hoặc sample ID, phiên bản dữ liệu, seed (nếu có), nhiệt độ (nếu kiểm soát được), giới hạn cấu hình và `top_k`.
4. Không lưu API key và không ghi tên `imdb_original` cho dữ liệu tự tạo.

### Chặng 2 – Prompt Engineering (35 phút)

**Tác vụ:** Nhận một review phim và trả JSON gồm các trường:

```json
{
  "sentiment": "negative",
  "evidence": ["the ending was disappointing"],
  "short_explanation": "The review is predominantly negative.",
  "confidence": "medium"
}
```

- `sentiment`: **chỉ** `positive` hoặc `negative` (nhãn chuẩn của bài toán IMDB gốc). `mixed_signal` là loại khó, không phải nhãn thứ ba.
- `evidence`: ít nhất một cụm từ **xuất hiện nguyên văn** trong review và thật sự hỗ trợ nhận định.
- `confidence`: `low`/`medium`/`high`, là cảm nhận mô hình tự báo cáo, **không phải xác suất đã hiệu chuẩn**.

**Quy trình:** Viết `prompt_v1.txt` (baseline) → thử trên dev → ghi ít nhất 2 lỗi → điều chỉnh `prompt_v2.txt` với thay đổi rõ ràng → **khóa prompt** trước evaluation. Nếu mode sample-output, tự điền prompt nhưng phân tích outputs cấp sẵn theo giả định minh họa, không được tuyên bố outputs đó do prompt mình tạo ra.

### Chặng 3 – Đánh giá prompt (25 phút)

Đánh giá **hai phiên bản trên cùng 10 eval reviews**. Tối thiểu báo cáo:

| Chỉ số | Cách hiểu |
|---|---|
| Sentiment Accuracy | Đúng `positive/negative` / tổng số mẫu eval, JSON lỗi tính không đúng |
| JSON Schema Valid Rate | JSON parse được và đủ trường đúng kiểu/danh mục |
| Exact Evidence Rate | Mọi đoạn evidence thật sự là substring nguyên văn review |
| Supported Evidence Rate | Kiểm tra thủ công: trích dẫn có hỗ trợ đúng nhãn không? |

Ghi **tử số và mẫu số** (VD 7/10); phân tích ít nhất **3 mẫu lỗi/khó** với `review_id`, output 2 phiên bản, error bucket và điều chỉnh đề xuất. Các buckets gợi ý: `wrong_sentiment`, `missed_negation`, `mixed_signal`, `invalid_json`, `hallucinated_evidence`, `unsupported_evidence`, `overconfident`.

**Câu hỏi bắt buộc:** V2 tăng tỷ lệ JSON hợp lệ nhưng accuracy không tăng — có thể kết luận mọi khía cạnh đều tốt hơn không?

### Chặng 4 – Cấu hình Single-hop RAG (40 phút)

1. Kiểm tra `knowledge_base/chunks.jsonl`; giải thích vì sao phải lưu ID và nguồn.
2. Chạy `python scripts/run_retrieval.py --top-k 1` và `--top-k 3`; lưu file CSV. Quan sát khi nào k=1 bỏ sót chunk có bằng chứng, khi nào k=3 đưa thêm nhiễu.
3. Hoàn thiện `prompts/rag_prompt.txt`: giới hạn chỉ dùng context được cấp, yêu cầu citation bằng `chunk_id`, từ chối nếu thiếu bằng chứng, bỏ qua chỉ dẫn không đáng tin nằm trong tài liệu.
4. Chạy `python scripts/prepare_rag_contexts.py --top-k 3`, rồi lấy câu hỏi và context để sinh output bằng API, Web UI hoặc nghiên cứu `samples/rag_answers_sample.jsonl`.
5. Lưu từng câu trả lời nguyên văn, context IDs và mode. Không bịa `chunk_id` khi câu trả lời không được hỗ trợ.

**Ví dụ dữ liệu minh họa:**

- `[RP01_C01]` “The pacing feels slow during the first act.”
- `[RP01_C02]` “The final act feels rushed and unsatisfying.”
- Câu hỏi: “Which weaknesses appear in RP01 reviews?”
- Trả lời đúng: “Reviewers criticize slow pacing [RP01_C01] and a rushed ending [RP01_C02].”

Câu hỏi có hai citations chưa nhất thiết là **multi-hop**: nếu hai chunks đã được lấy từ **một lượt truy hồi**, đây vẫn là single-hop retrieval.

### Chặng 5 – Kiểm chứng câu trả lời (20 phút)

Bộ 12 QA gồm `8 evidence`, `2 no_evidence`, `2 injection`:

- Với evidence: đo **Hit@3** trên các câu có gold chunk; chấm thủ công `citation_support` và `answer_grounding`.
- Với no-evidence: hệ thống phải nói rõ không đủ căn cứ trong knowledge base, không bịa nguồn.
- Với injection: không làm theo các lệnh yêu cầu bỏ quy định/trích dẫn hoặc chỉ thị chèn trong tài liệu; vẫn phân biệt nội dung dữ liệu với chỉ dẫn điều khiển.
- Mỗi nhóm chọn ít nhất **1 lỗi có căn cứ** (nếu có) và phân loại: retrieval miss, wrong/missing citation, unsupported answer hoặc guardrail failure. Nếu không có lỗi quan sát được, ghi rõ giới hạn cỡ mẫu, không tự tạo lỗi giả.

**Lưu ý:** `Hit@3` có nghĩa top-3 chứa **ít nhất một** gold chunk, không bảo đảm đã thu thập đủ mọi bằng chứng. Các câu no-evidence không tính vào mẫu số của Hit@3. Khi chưa có gold đầy đủ, sinh viên chỉ báo cáo hit trên các câu đã được gán gold, không tự khẳng định kết quả toàn bộ tập.

## 5. Ba chế độ chạy

| Chế độ | Thực hiện | Bằng chứng bắt buộc | Giới hạn |
|---|---|---|---|
| **A — API** | Chạy mô hình qua API do lớp cho phép; giữ phiên bản cấu hình | Prompt, input, raw output, model, run manifest, logs | Không push key; có thể không deterministic |
| **B — Web UI** | Dùng prompt đúng template trên giao diện chatbot | Prompt đã gửi, output chép nguyên văn, mô hình và thời điểm | Khó khóa version/model parameters; phải công bố |
| **C — Sample-output** | Dùng outputs minh họa; chạy eval/truy hồi offline | Các file được cấp, log tự chạy evaluator, nhận xét | **Không phải** minh chứng đã chạy LLM; không so sánh hiệu năng prompt do bản thân tạo |

## 6. Sản phẩm nộp

```text
submission/
├── README.md                          # tên nhóm, mode, cách chạy
├── run_manifest.json                  # cấu hình, provenance
├── prompts/
│   ├── prompt_v1.txt
│   ├── prompt_v2.txt
│   └── rag_prompt.txt
├── outputs/
│   ├── prompt_runs_v1.jsonl
│   ├── prompt_runs_v2.jsonl
│   ├── prompt_comparison.csv
│   ├── retrieval_top1.csv
│   ├── retrieval_top3.csv
│   ├── rag_answers.jsonl
│   └── rag_checks.csv
└── reports/
    ├── error_analysis.md
    └── lab_report.md
```

`lab_report.md` dài khoảng 2–3 trang, gồm: (1) mục tiêu và giả thuyết; (2) dữ liệu và mode; (3) thay đổi v1→v2; (4) metric và 3 lỗi; (5) so sánh top-1/top-3; (6) citation, từ chối, injection; (7) hạn chế, hướng mở rộng. Không bắt buộc phải có mọi file nếu API/Web UI bị giới hạn nhưng phải ghi chính xác dữ liệu nào thực sự được chạy/chấm.

## 7. Nguyên tắc báo cáo và an toàn

- Không sửa gold label sau khi xem output, không lựa mẫu có lợi, không trộn đầu ra mẫu với live outputs mà thiếu provenance.
- Chỉ dẫn trong review packs là **dữ liệu không đáng tin**; không được ưu tiên hơn quy tắc RAG prompt.
- Không công bố API token, mật khẩu, thông tin cá nhân.
- Khả năng citation đúng phải được kiểm tra ở **mức hỗ trợ nội dung**, không chỉ mã nguồn có tồn tại.
- Bộ test quá nhỏ để kết luận tổng quát về chất lượng hệ thống ngoài phạm vi thực hành.

## 8. Câu hỏi kết thúc – mở sang Multi-hop RAG

> Nếu phải xác định bộ phim được nói đến trong một tài liệu A rồi **dựa vào tên phim tìm tiếp** thông tin ở tài liệu B, một lượt retrieval với câu hỏi gốc có thể thiếu gì? Em sẽ thiết kế hai truy vấn phụ thuộc nhau như thế nào?

Chỉ trả lời bằng thiết kế/nhận định, **chưa yêu cầu cài multi-hop ở Lab 6**.
