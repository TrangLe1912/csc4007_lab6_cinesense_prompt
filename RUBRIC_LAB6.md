# Rubric Lab 6 (thang 10 điểm) – chỉ dành cho bài thực hành tích hợp

Đây là **rubric hoạt động lab độc lập**, chưa ánh xạ OBE hoặc thay thế bất kỳ rubric chính thức nào của học phần.

| Hạng mục | Điểm | Đạt yêu cầu khi |
|---|---:|---|
| Prompt v1/v2, thay đổi có chủ đích | 2.5 | Có 2 prompt khác nhau, đúng schema, lý do sửa dựa trên tối thiểu 2 lỗi dev |
| Evaluation và phân tích lỗi | 2.0 | Cùng eval set, báo cáo tử/mẫu số, JSON/schema, accuracy, exact evidence; >=3 ca lỗi sâu |
| Cấu hình retrieval và RAG | 2.0 | Chạy top-1/top-3, tạo context, có RAG prompt và câu trả lời gắn chunks |
| Citation, no-evidence, prompt injection | 2.0 | Kiểm thử đúng loại ca, có kiểm tra support thủ công và nhận diện sai sót |
| Báo cáo, tái hiện và minh bạch nguồn | 1.5 | Manifest, báo cáo, file output phù hợp mode, phân biệt đầu ra mẫu/live, không lộ credentials |
| **Tổng** | **10.0** | |

## Thang mô tả gợi ý

- **Mức đầy đủ (>=80% của từng tiêu chí):** hoạt động đúng, có minh chứng rõ, giải thích nguyên nhân/giới hạn.
- **Mức cơ bản (50–<80%):** chạy được nhiệm vụ chính nhưng thiếu phân tích hoặc một phần minh chứng.
- **Mức chưa đạt (<50%):** không có bằng chứng, không thực hiện hoặc kết luận không gắn dữ liệu.

### Nguyên tắc công bằng giữa ba chế độ

API/Web UI có thể cung cấp **bằng chứng chạy mô hình**. Sample-output chỉ có thể chứng minh **khả năng đọc, đánh giá và phân tích đầu ra được cấp**, không thể được mô tả là người học đã chạy LLM. Giảng viên chấm phần đánh giá/kỹ thuật thực sự làm được và yêu cầu khai báo giới hạn, không tự giả định mode C có bằng chứng inference tương đương. Nếu muốn bảo đảm trọn điểm ở hạng mục chạy prompt/RAG, giảng viên có thể cấp một buổi demo ngắn hoặc cho sinh viên tự chạy bổ sung.
