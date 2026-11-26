# D-002: Lựa chọn và quản lý môi trường phân tích dữ liệu Python

Ngày: 26/11/2026 | Trạng thái: Đã chốt  
Liên quan: G-24.11.26 (Mục 6.2); Issue #2

## Bối cảnh
Nghiên cứu đòi hỏi sử dụng nhiều thư viện chuyên sâu về suy luận nhân quả và học máy (scikit-learn, LightGBM, scikit-uplift, CausalML, EconML, SHAP) cùng các công cụ xử lý dữ liệu lớn ở local (DuckDB, Polars, PyArrow). Các thư viện causal machine learning thường có phụ thuộc biên dịch C/C++ phức tạp (Cython, OpenMP) và có thể gây xung đột phiên bản nếu không quản lý chặt chẽ. Cần một môi trường chuẩn hóa, có thể tái lập hoàn toàn trên máy mới.

## Các phương án
1. **Python 3.11 qua Conda/Mamba kèm lock file:**
   - *Ưu điểm:* Quản lý tốt các thư viện phụ thuộc C/Fortran qua `conda-forge`; hỗ trợ xuất chính xác danh mục gói; tương thích cao với CausalML và EconML.
   - *Nhược điểm:* Dung lượng cài đặt môi trường ban đầu tương đối lớn.
2. **Python Virtualenv (venv/pip) đơn thuần:**
   - *Ưu điểm:* Nhẹ, tích hợp sẵn trong Python standard library.
   - *Nhược điểm:* Dễ gặp lỗi build C++ trên một số hệ điều hành khi cài đặt CausalML / EconML; khó quản lý xung đột binary.
3. **Docker Container toàn diện cho Data Science:**
   - *Ưu điểm:* Cô lập tuyệt đối môi trường hệ điều hành.
   - *Nhược điểm:* Phức tạp khi tương tác trực tiếp với GPU/IDE và tiêu tốn tài nguyên máy tính cá nhân khi chạy EDA tương tác.

## Quyết định
- Chọn **Python 3.11** quản lý qua Conda (`environment.yml`), kết hợp `pip` cho các thư viện uplift chuyên biệt (`scikit-uplift`, `causalml`, `econml`, `shap`).
- Khóa toàn bộ phiên bản phụ thuộc trong tệp `environment-lock.yml`.
- Cố định `SEED = 42` trên toàn bộ pipeline (numpy, random, lightgbm, sklearn) để đảm bảo mọi kết quả tái lập tuyệt đối.
- Tách biệt rõ ràng: code thí nghiệm trong `lab/notebooks/`, code dùng chung đóng gói vào `lab/src/uplift_lab/`.

## Lý do và bằng chứng
- Thử nghiệm thực tế cho thấy Python 3.11 là phiên bản cân bằng nhất: tương thích hoàn toàn với scikit-uplift 0.5.1, LightGBM, SHAP, DuckDB và Polars.
- Tệp `environment-lock.yml` ghi lại chính xác từng commit/build hash của các thư viện, cho phép tái lập từ máy trống theo đúng yêu cầu Mục 6.1 và 6.2.

## Hệ quả
- Khi Thầy kiểm tra code, chỉ cần chạy `conda env create -f environment.yml` là có thể chạy ngay notebook mà không phát sinh lỗi phiên bản.
- Nếu CausalML và EconML phát sinh xung đột trong các giai đoạn sau (Giai đoạn 2), sẵn sàng tách nhánh môi trường thử nghiệm riêng cho causal forest mà không ảnh hưởng pipeline chính.
