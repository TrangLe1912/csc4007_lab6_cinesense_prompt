# Nguồn dữ liệu

- Mọi review trong `prompt_*.csv` là **câu mô phỏng do bộ kit tạo**, chỉ dùng minh họa kỹ thuật, **KHÔNG** phải review IMDB gốc.
- Mọi review pack và chunks là `synthetic_teaching_example`, được thiết kế để thử truy hồi/citation, không gán cho phim/tác giả thực.
- Bộ câu hỏi QA cũng được dựng để kiểm thử. Giảng viên có thể thay `prompt_dev.csv`, `prompt_eval.csv` bằng mẫu **IMDB gốc có nguồn** khi triển khai chính thức.
- `samples/` không phải kết quả chạy LLM thực và không được trình bày như số liệu thực nghiệm thật.
- Chỉ dùng `data/qa_gold_practice.csv` cho việc minh họa Hit@k; bảng gold đầy đủ nằm riêng ở phía giảng viên.
