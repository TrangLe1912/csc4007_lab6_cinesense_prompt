# CSC4007 Lab 6 — Mamba/Long-sequence Benchmark

Lab này dùng một giao thức benchmark có kiểm soát để phân tích trade-off của RNN, LSTM, GRU, Transformer và Mamba/SSM khi độ dài chuỗi tăng.

> **Giới hạn quan trọng:** benchmark mặc định dùng token tổng hợp để đo khả năng mở rộng về thời gian và bộ nhớ. Nó **không đo chất lượng ngôn ngữ**. Metric chất lượng từ các lab trước phải được ghi riêng trong `data/task_metrics_template.csv`.

## Kết quả học tập

Sau lab, sinh viên có thể:

- chạy cùng một giao thức trên nhiều mô hình và độ dài chuỗi;
- lưu cấu hình, latency, throughput, bộ nhớ và số tham số;
- phân biệt bằng chứng về chi phí tính toán với bằng chứng về chất lượng tác vụ;
- lập luận lựa chọn mô hình theo metric, tài nguyên, độ dài chuỗi và bối cảnh.

Ánh xạ: **LLO07 → CLO3, CLO4**; kết quả là một phần minh chứng của **A2.2**.

## Cài đặt nhanh

Yêu cầu Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Chạy smoke test không cần Mamba:

```bash
python run_lab6.py --smoke --models rnn,lstm,gru,transformer
pytest -q
```

Chạy benchmark chính:

```bash
python run_lab6.py \
  --sequence-lengths 128,256,512,1024 \
  --models rnn,lstm,gru,transformer,mamba \
  --batch-size 8 \
  --hidden-size 64 \
  --warmup 3 \
  --repeats 10 \
  --device auto
```

Kết quả được ghi vào `outputs/`:

- `benchmark.csv`: dữ liệu thô theo mô hình và độ dài chuỗi;
- `run_config.json`: cấu hình và thông tin môi trường;
- `tradeoff_summary.md`: bảng tóm tắt để bắt đầu phân tích.

## Cài Mamba thật (tùy môi trường)

Mamba là dependency tùy chọn vì gói chính thức thường cần Linux, CUDA tương thích và compiler phù hợp.

```bash
pip install -r requirements-mamba.txt
python run_lab6.py --models mamba --include-mamba yes --device cuda
```

Luôn đối chiếu hướng dẫn mới nhất trong [repository chính thức state-spaces/mamba](https://github.com/state-spaces/mamba). Nếu chưa cài được, script ghi `status=not_installed`; không được đổi nhãn này thành kết quả đã chạy. Có thể thảo luận kết quả tham khảo nếu ghi rõ nguồn, phần cứng và tách khỏi kết quả tự chạy.

## Giao thức so sánh công bằng

Giữ nguyên giữa các mô hình:

- batch size, hidden size, số lớp, vocabulary và device;
- warmup, số lần lặp và seed;
- độ dài chuỗi và kiểu dữ liệu;
- phiên bản phần mềm và điều kiện phần cứng.

Số tham số giữa các kiến trúc không hoàn toàn bằng nhau; vì vậy `parameters` luôn được xuất để người học nêu giới hạn này. CPU memory dùng mức tăng RSS lấy mẫu (hoặc high-water RSS khi sandbox không cho truy cập process), còn CUDA dùng peak allocated memory của PyTorch; trường `memory_method` cho biết cách đo.

## Nhiệm vụ

Xem [ASSIGNMENT.md](ASSIGNMENT.md) và [RUBRIC.md](RUBRIC.md). Tối thiểu cần:

1. chạy benchmark trên ít nhất bốn độ dài chuỗi;
2. so sánh RNN/LSTM/GRU/Transformer và thử Mamba khi môi trường cho phép;
3. bổ sung metric chất lượng tác vụ từ lab trước;
4. hoàn thiện `reports/analysis_report.md` với kết luận có giới hạn.

## Cấu trúc repo

```text
.
├── run_lab6.py
├── src/
│   ├── models.py
│   └── benchmark.py
├── data/task_metrics_template.csv
├── reports/analysis_report.md
├── tests/
├── ASSIGNMENT.md
└── RUBRIC.md
```

## Tài liệu chính

- Gu & Dao, [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752)
- [Official Mamba implementation](https://github.com/state-spaces/mamba)
