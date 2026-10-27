# CSC4007 – Lab 6: Prompt Engineering & RAG (Guided Scaffold)

**Thời lượng:** 135 phút • **Ngữ cảnh:** CineSense/IMDB • **Ba chế độ:** API / Web UI / đầu ra mẫu.

> Bản đi kèm có ngữ liệu **GIẢ LẬP CHỈ ĐỂ DẠY/SMOKE TEST**, không phải các review thật tải từ IMDB, không phải kết quả suy luận thật của LLM. Giảng viên nên thay phần review CSV bằng trích mẫu IMDB đúng nguồn trước khi phát chính thức nếu muốn so sánh trên IMDB gốc. Knowledge base CineSense minh họa có thể giữ lại để kiểm tra RAG.

## Cài đặt

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/smoke_test.py
```

## Đường chạy cơ bản

```bash
python scripts/run_retrieval.py --top-k 1
python scripts/run_retrieval.py --top-k 3
python scripts/prepare_rag_contexts.py --top-k 3
python scripts/evaluate_prompt.py --v1 samples/prompt_runs_v1_sample.jsonl --v2 samples/prompt_runs_v2_sample.jsonl
python scripts/evaluate_rag.py --answers samples/rag_answers_sample.jsonl
```

Lệnh trên chạy **offline** trên dữ liệu và đầu ra mẫu. Đây là đường kiểm thử pipeline, **không phải bằng chứng đã gọi LLM**.

## Cách làm 3 chế độ

- **API:** thiết lập **biến môi trường** theo `.env.example` (file `.env` không được tự động nạp; trên macOS/Linux có thể chạy `set -a; source .env; set +a`), rồi chạy `python scripts/run_prompt_api.py --version v1` (sau đó v2). `LLM_API_URL` phải là URL endpoint OpenAI-compatible `/chat/completions` mà người học được phép sử dụng. Không đưa API key lên repo. Bài RAG có thể chạy bằng lệnh `python scripts/run_rag_api.py` nếu đã cấu hình API.
- **Web UI:** chạy `python scripts/prepare_web_prompts.py`, mở `outputs/web_prompts/`, gửi lần lượt vào giao diện; lưu nguyên văn phản hồi vào JSONL đúng schema như trong `samples/`. Không tự động hóa website bằng script này.
- **Sample-output:** dùng `samples/*_sample.jsonl` để chấm và phân tích; đánh dấu nguồn `provided_sample_not_live_inference`. Sinh viên **vẫn tự viết ba prompt** và phân tích giới hạn, nhưng không được tuyên bố đã chạy inference mới.

Xem `ASSIGNMENT.md`, `RUBRIC_LAB6.md` và `reports/lab_report_template.md`.

## Cấu trúc

- `data/`: 5 dev, 10 eval, 5 stress (đều là ví dụ giả lập) và 12 câu hỏi QA.
- `knowledge_base/`: 10 mini packs × 2 chunks có ID và nguồn.
- `src/retriever.py`: TF-IDF + cosine retrieval được cung cấp sẵn.
- `prompts/`: ba prompt người học hoàn thiện.
- `samples/`: đầu ra được dựng để luyện đánh giá, không phải output API thật.
- `scripts/`: kiểm thử dữ liệu, truy hồi, chuẩn bị context, chấm cú pháp và chạy API khi được cấu hình.
- `outputs/`: kết quả được tạo khi chạy; không nộp log giả làm thực nghiệm.

**Lưu ý:** Gold QA đầy đủ và hướng dẫn giảng viên được phát riêng, không nằm trong gói student.

## Lịch sử phiên bản

Repo hiện được dùng cho Lab 6 tích hợp Prompt Engineering + RAG. Bản Lab 6 Mamba trước khi cập nhật đã được giữ ở nhánh [`archive/lab6-mamba-before-prompt-rag-2026-10-27`](https://github.com/TrangLe1912/csc4007_lab6_cinesense_prompt/tree/archive/lab6-mamba-before-prompt-rag-2026-10-27). Không có đáp án gold QA dành riêng cho giảng viên trong repo công khai.
