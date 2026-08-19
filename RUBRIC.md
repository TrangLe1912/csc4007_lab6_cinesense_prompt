# Rubric Lab 6 — 10 điểm

| Hạng mục | Điểm | Đạt đầy đủ khi |
|---|---:|---|
| Tái lập môi trường | 1.0 | Có config, phiên bản, device, seed và smoke test chạy được |
| Thiết kế benchmark | 2.0 | Cùng điều kiện, tối thiểu 4 độ dài chuỗi, warmup/repeats hợp lý |
| Thực thi và bằng chứng | 2.0 | Có kết quả RNN/LSTM/GRU/Transformer; trạng thái Mamba trung thực; giữ log lỗi/OOM |
| Metric chất lượng | 2.0 | Dùng dữ liệu NLP thật, ghi dataset/split/metric/source; không trộn với synthetic benchmark |
| Phân tích trade-off | 2.0 | So sánh metric, latency, memory, parameters, độ dài chuỗi và bối cảnh; nêu giới hạn |
| Tài liệu hóa | 1.0 | Báo cáo rõ, file đúng cấu trúc, lệnh chạy tái lập được |

## Lỗi nghiêm trọng

- Ghi kết quả Mamba đã chạy khi dependency/model chưa chạy thật: không tính điểm phần thực thi Mamba và trừ minh chứng.
- So sánh bằng các điều kiện khác nhau mà không khai báo: tối đa 50% điểm thiết kế benchmark.
- Dùng latency synthetic để kết luận chất lượng NLP: không tính điểm lập luận tương ứng.

