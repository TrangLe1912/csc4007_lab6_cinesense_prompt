# Lab 6 – CineSense Prompt Evaluation Scaffold

## 1. Mục đích

Bộ này là **lab scaffold tối thiểu**, không phải starter kit hoàn chỉnh.

Sinh viên cần tự thiết kế prompt, chạy thử nghiệm, phân tích lỗi và cải tiến prompt trên ngữ cảnh IMDB Movie Review Dataset đã được dùng xuyên suốt từ Lab 1 đến Lab 5.

Lab 6 nối tiếp Lab 5 về Transformer/self-attention/fine-tuning bằng cách đặt câu hỏi thực tế:

> Khi dùng LLM cho tác vụ phân tích review phim, làm sao biết prompt có đáng tin cậy hay không?

Thông điệp chính của lab:

> Prompt Engineering không chỉ là viết một câu lệnh hay. Đó là một vòng lặp gồm: thiết kế prompt → chạy thử → đo lường → phân tích lỗi → cải tiến prompt.

## 2. Kết quả học tập mong đợi

Sau lab này, sinh viên có thể:

1. Thiết kế prompt cho tác vụ phân tích sentiment của review phim.
2. So sánh prompt baseline, prompt cải tiến và prompt có tư duy Chain-of-Thought.
3. Yêu cầu LLM trả output có cấu trúc JSON.
4. Đánh giá output bằng metric cụ thể thay vì nhận xét cảm tính.
5. Phân tích lỗi theo error bucket.
6. Nhận xét khi nào LLM đáng tin và khi nào không đáng tin.

## 3. Cấu trúc thư mục

```text
lab6_cinesense_prompt_scaffold/
├── data/
│   ├── imdb_sample_50.csv
│   └── student_testset_template.csv
├── prompts/
│   ├── prompt_template_v1.txt
│   ├── prompt_template_v2.txt
│   ├── prompt_template_v3_cot.txt
│   └── system_prompt_optional.txt
├── eval/
│   ├── eval_template.csv
│   └── error_bucket_guide.md
├── outputs_sample/
│   ├── result_v1_sample.csv
│   ├── result_v2_sample.csv
│   └── result_v3_cot_sample.csv
├── scripts/
│   └── run_prompt_eval_skeleton.py
├── submissions/
│   └── error_analysis_template.md
├── ASSIGNMENT.md
└── RUBRIC.md
```

## 4. Dữ liệu mẫu

File `data/imdb_sample_50.csv` gồm 50 review ngắn theo phong cách IMDB, được tạo để minh họa cho lab. Đây không phải dữ liệu gốc của IMDB.

Sinh viên có thể:

- dùng file mẫu có sẵn để chạy thử;
- hoặc thay thế bằng một mẫu lấy từ IMDB dataset đã dùng trong các bài trước.

Các cột chính:

| Cột | Ý nghĩa |
|---|---|
| review_id | Mã review |
| review_text | Nội dung review |
| gold_sentiment | Nhãn chuẩn: positive hoặc negative |
| expected_aspects | Một số khía cạnh đáng chú ý |
| difficulty | Mức độ dễ/khó của mẫu |
| source_note | Ghi chú nguồn |

Sinh viên tạo testset riêng bằng file:

```text
data/student_testset_template.csv
```

Testset nên có 20–50 review, bao gồm các loại: `easy`, `mixed`, `ambiguous`, `keyword_trap`, `long_review`.

## 5. Nhiệm vụ chính

### Bước 1: Chọn tác vụ

Tối thiểu chọn tác vụ:

> Phân loại sentiment của review phim: positive/negative.

Nhóm khá có thể mở rộng thêm:

- trích xuất aspect;
- giải thích bằng chứng;
- đánh giá confidence;
- phát hiện hallucination;
- phân tích lỗi do keyword trap hoặc mixed review.

### Bước 2: Viết Prompt v1 – Baseline Prompt

Mở file:

```text
prompts/prompt_template_v1.txt
```

Prompt v1 là prompt ngắn, trực tiếp, dùng để tạo baseline.

### Bước 3: Viết Prompt v2 – Improved Prompt

Mở file:

```text
prompts/prompt_template_v2.txt
```

Prompt v2 cần cải tiến có chủ đích so với v1, ví dụ:

- yêu cầu chỉ dùng thông tin trong review;
- không bịa thêm thông tin về phim, diễn viên, đạo diễn, giải thưởng;
- trích evidence đúng nguyên văn từ review;
- xử lý review có cả khen và chê;
- thêm confidence.

### Bước 4: Viết Prompt v3 – CoT-inspired Prompt

Mở file:

```text
prompts/prompt_template_v3_cot.txt
```

Prompt v3 dùng tư duy Chain-of-Thought ở mức kiểm soát được.

Lưu ý quan trọng:

- Không yêu cầu LLM in ra toàn bộ chuỗi suy luận dài.
- Nên yêu cầu LLM phân tích nội bộ theo các bước.
- Output cuối cùng vẫn phải là JSON hợp lệ, ngắn gọn, dễ đánh giá.

Ví dụ tư duy mong muốn:

```text
Identify positive clues → identify negative clues → decide which attitude dominates → check exact evidence → return JSON only.
```

### Bước 5: Chạy thử nghiệm

Chạy cả 3 prompt trên cùng một testset 20–50 review.

Có ba cách thực hiện:

1. Dùng ChatGPT/Gemini/Claude qua web UI.
2. Dùng API như Gemini API, Groq API, OpenRouter, Ollama local API.
3. Dùng file output mẫu nếu lỗi mạng hoặc chưa cấu hình được API.

Không bắt buộc dùng API nếu mục tiêu chính của buổi học là đánh giá prompt.

### Bước 6: Đánh giá output

Dùng:

```text
eval/eval_template.csv
eval/error_bucket_guide.md
```

Mỗi dòng cần xác định:

- sentiment đúng hay sai;
- JSON có hợp lệ không;
- evidence có lấy đúng từ review không;
- có hallucination không;
- có dùng outside knowledge không;
- confidence có hợp lý không;
- lỗi thuộc bucket nào.

### Bước 7: Viết báo cáo phân tích lỗi

Dùng:

```text
submissions/error_analysis_template.md
```

Báo cáo phải chỉ ra prompt nào tốt hơn, tốt hơn ở loại lỗi nào, và CoT có thật sự giúp ích không.

## 6. Yêu cầu nộp

```text
lab6_submission/
├── prompt_v1.txt
├── prompt_v2.txt
├── prompt_v3_cot.txt
├── testset.csv
├── result_v1.csv
├── result_v2.csv
├── result_v3_cot.csv
├── eval_v1.csv
├── eval_v2.csv
├── eval_v3_cot.csv
└── error_analysis.md
```

## 7. Metric tối thiểu cần báo cáo

| Metric | Ý nghĩa |
|---|---|
| Accuracy | Tỷ lệ dự đoán đúng sentiment |
| Valid JSON rate | Tỷ lệ output là JSON hợp lệ |
| Evidence exactness rate | Tỷ lệ evidence được trích đúng nguyên văn từ review |
| Hallucination count | Số output bịa thêm thông tin không có trong review |
| Outside knowledge count | Số output dùng kiến thức ngoài review |
| Overconfidence count | Số output quá tự tin với review nhập nhằng |

Bảng so sánh nên có dạng:

| Metric | Prompt v1 | Prompt v2 | Prompt v3 CoT | Comment |
|---|---:|---:|---:|---|
| Accuracy | | | | |
| Valid JSON rate | | | | |
| Evidence exactness rate | | | | |
| Hallucination count | | | | |
| Outside knowledge count | | | | |
| Overconfidence count | | | | |

## 8. Tiêu chí đánh giá tóm tắt

| Tiêu chí | Điểm |
|---|---:|
| Testset 20–50 mẫu, có đủ easy/mixed/ambiguous/keyword-trap | 1.5 |
| Prompt v1, v2, v3 CoT có khác biệt rõ ràng | 2.0 |
| Chạy đủ 3 prompt và lưu output đúng định dạng | 1.5 |
| Đánh giá bằng metric rõ ràng | 2.0 |
| Phân tích lỗi bằng error bucket, có ví dụ cụ thể | 2.0 |
| Reflection tốt về CoT và độ tin cậy của prompt | 1.0 |
| **Tổng** | **10.0** |

Xem chi tiết trong:

```text
RUBRIC.md
```

## 9. Lưu ý quan trọng

Không đánh giá prompt bằng cảm giác. Cần có bằng chứng qua testset, bảng lỗi và ví dụ cụ thể.

Không kết luận “CoT tốt hơn” chỉ vì prompt dài hơn. Cần so sánh bằng metric và phân tích lỗi.

Một prompt tốt không chỉ dự đoán đúng nhãn, mà còn cần:

- trả output đúng format;
- trích evidence đúng;
- không hallucinate;
- không quá tự tin với review nhập nhằng;
- giải thích ngắn gọn và có căn cứ.
