# Cost-Based Query Optimizer for Distributed Databases

Mô phỏng bộ tối ưu truy vấn dựa trên chi phí (Cost-Based Optimizer - CBO) trong môi trường cơ sở dữ liệu phân tán nhằm lựa chọn kế hoạch thực thi truy vấn có chi phí thấp nhất.

---

## Giới thiệu

Dự án triển khai một bộ tối ưu truy vấn dựa trên chi phí cho cơ sở dữ liệu phân tán.

Hệ thống đánh giá nhiều kế hoạch thực thi truy vấn khác nhau, tính toán tổng chi phí thực thi của từng phương án và tự động lựa chọn kế hoạch tối ưu.

Các khái niệm được minh họa trong dự án:

- Xử lý truy vấn phân tán
- Cost-Based Optimization
- Communication Cost
- CPU Cost
- I/O Cost
- Semi-Join
- Distributed Query Processing

---

## Cấu trúc dự án

```text
.
├── data/
│   └── generator.py
│
├── optimizer/
│   ├── cbo.py
│   ├── cost_model.py
│   ├── plan_a.py
│   └── plan_b.py
│
├── report/
│   ├── analyzer.py
│   └── cost_comparison.png
│
├── simulation/
│   ├── executor.py
│   └── config.py
│
├── main.py
├── README.md
└── requirements.txt
```

## Yêu cầu

- Python 3.10 trở lên

Kiểm tra phiên bản Python:

```bash
python --version
```

---

## Cài đặt

Clone repository:

```bash
git clone <repository-url>
cd <repository-name>
```

Không yêu cầu cài đặt thêm thư viện bên ngoài.

---

## Chạy chương trình

Thực thi lệnh:

```bash
python main.py
```

---

## Kết quả

Chương trình sẽ:

1. Sinh các kế hoạch thực thi truy vấn khả thi.
2. Tính toán chi phí của từng kế hoạch.
3. So sánh tổng chi phí.
4. Chọn kế hoạch có chi phí thấp nhất.

Ví dụ:

```text
=== Distributed Query Optimization ===

Plan A Cost: 12000

Plan B Cost: 3500

Selected Plan: Plan B
```

---

## Mô hình chi phí

Chi phí thực thi được tính dựa trên các thành phần:

- Communication Cost (chi phí truyền dữ liệu)
- CPU Cost (chi phí xử lý)
- I/O Cost (chi phí truy xuất dữ liệu)

Tổng chi phí của mỗi kế hoạch được sử dụng để đưa ra quyết định lựa chọn.

---

## Kịch bản minh họa

### Plan A - Ship Whole Relation

Toàn bộ dữ liệu được chuyển từ một site sang site khác trước khi thực hiện phép Join.

Ưu điểm:

- Đơn giản
- Ít bước xử lý

Nhược điểm:

- Chi phí truyền dữ liệu lớn khi dữ liệu có kích thước lớn

### Plan B - Semi Join

Chỉ các thuộc tính cần thiết được gửi trước để lọc dữ liệu từ xa, sau đó chỉ truyền về những bản ghi cần thiết.

Ưu điểm:

- Giảm lượng dữ liệu truyền qua mạng
- Hiệu quả với tập dữ liệu lớn

Nhược điểm:

- Phát sinh thêm bước xử lý và trao đổi thông tin

---

## Tài liệu tham khảo

Özsu, M. T., & Valduriez, P.

*Principles of Distributed Database Systems* (3rd Edition).

Springer, 2011.

---

## Thông tin sinh viên

- Họ và tên: Huỳnh Minh Tâm
- Ngành: Công nghệ Thông tin
- Môn học: Cơ sở dữ liệu phân tán
- Đề tài: Cost-Based Query Optimizer for Distributed Databases