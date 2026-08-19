# Bài tập Lab 6

## Câu hỏi thực nghiệm

Khi độ dài chuỗi tăng, latency, throughput và bộ nhớ của RNN/LSTM/GRU/Transformer/Mamba thay đổi ra sao? Mô hình nào phù hợp với bối cảnh bạn chọn, xét đồng thời chất lượng tác vụ và nguồn lực?

## Phần A — Tái lập môi trường (1 điểm)

- Chạy `pytest -q` và smoke benchmark.
- Lưu `outputs/run_config.json`.
- Ghi rõ CPU/GPU, phiên bản Python/PyTorch và tình trạng Mamba.

## Phần B — Benchmark có kiểm soát (4 điểm)

- Chọn ít nhất bốn độ dài chuỗi, trong đó độ dài lớn nhất phải phù hợp với tài nguyên máy.
- Giữ nguyên batch size, hidden size, số lớp, seed, warmup và repeats.
- Chạy RNN, LSTM, GRU và Transformer.
- Chạy Mamba thật khi môi trường hỗ trợ. Nếu không, giữ `not_installed` và giải thích.
- Không xóa các hàng lỗi/OOM; chúng cũng là bằng chứng về giới hạn.

## Phần C — Chất lượng tác vụ (2 điểm)

Điền `data/task_metrics_template.csv` bằng kết quả từ dữ liệu NLP thật ở các lab trước. Ghi rõ dataset, split, metric và nguồn file/log. Không điền metric giả vào kết quả synthetic.

## Phần D — Phân tích trade-off (3 điểm)

Hoàn thiện `reports/analysis_report.md`:

- mô tả điều kiện thực nghiệm;
- nhận xét xu hướng theo độ dài chuỗi;
- đối chiếu compute với metric chất lượng;
- nêu sai số đo, giới hạn và mối đe dọa tới tính hợp lệ;
- chọn mô hình cho một bối cảnh cụ thể và bảo vệ lựa chọn bằng bằng chứng.

## File cần nộp

- mã nguồn đã chỉnh nếu có;
- `outputs/benchmark.csv`;
- `outputs/run_config.json`;
- `outputs/tradeoff_summary.md`;
- `data/task_metrics_template.csv` đã điền;
- `reports/analysis_report.md` đã hoàn thiện.

