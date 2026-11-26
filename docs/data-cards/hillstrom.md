# Data card: Hillstrom (MineThatData E-Mail Analytics and Data Mining Challenge)

## 1. Nguồn
- Tác giả: Kevin Hillstrom (MineThatData); bài đăng ngày 20/3/2008
- Trang gốc: Hillstrom, K. (2008, March 20). The MineThatData e-mail analytics and data mining challenge [Blog post]. MineThatData. https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html
- Điều khoản sử dụng: Trang gốc không nêu giấy phép hay điều kiện sử dụng dữ liệu (đã kiểm tra ngày 26/11/2026). Em chỉ dùng cho nghiên cứu học thuật, không phân phối lại dữ liệu, và trích dẫn nguồn. Nếu cần công bố dữ liệu, sẽ xin phép tác giả.
- Mục đích gốc: thử thách phân tích email marketing; các câu hỏi gốc gồm email nào hiệu quả hơn, doanh thu gia tăng mỗi khách, và chọn 10.000 khách nhận email tốt nhất.

## 2. Cách tải
- Hàm `sklift.datasets.fetch_hillstrom(target_col=..., data_home="data/raw")` (scikit-uplift=0.5.1). Thư viện tải bản sao dữ liệu; tên cột và quy mô khớp mô tả của trang gốc
- Ngày tải: 26/11/2026
- File lưu: `data/raw/hillstorm_no_indices.csv.gz` (tên do thư viện đặt). KHÔNG commit (đã .gitignore)

## 3. Quy mô và chất lượng
- 64.000 khách đã mua trong 12 tháng gần nhất, tham gia một thử nghiệm email
- 13 cột sau khi ghép trong notebook: 8 đặc trưng, 3 biến kết quả, `segment` (nhóm email gốc) và `group` (tự tạo)
- Không có giá trị thiếu
- 6.562 dòng trùng toàn bộ nhưng dữ liệu không có mã khách hàng nên KHÔNG loại bỏ
- Mỗi dòng là một khách hàng; không có mã định danh

## 4. Can thiệp (treatment)
Mỗi khách được gán ngẫu nhiên một trong ba nhóm (cột `segment`), mỗi nhóm khoảng 1/3:

| segment | group (đặt trong notebook) | n | tỷ lệ |
|---|---|---|---|
| Mens E-Mail | men | 21.307 | 33,29% |
| Womens E-Mail | women | 21.387 | 33,42% |
| No E-Mail | control | 21.306 | 33,29% |

Can thiệp là một chiến dịch email quảng bá hàng nam hoặc hàng nữ, không phải mã giảm giá.

## 5. Biến (đã đối chiếu với trang gốc ngày 26/11/2026)

| Biến | Loại | Ý nghĩa |
|---|---|---|
| recency | số | Số tháng từ lần mua gần nhất |
| history_segment | phân loại | Nhóm chi tiêu trong năm qua |
| history | số | Số tiền đã chi trong năm qua (đô la) |
| mens / womens | 0/1 | Đã mua hàng nam / nữ trong năm qua |
| zip_code | phân loại | Urban / Suburban / Rural (trong dữ liệu viết "Surburban") |
| newbie | 0/1 | Khách mới trong 12 tháng qua |
| channel | phân loại | Các kênh khách đã mua trong năm qua |
| visit | 0/1 | Ghé website trong 2 tuần sau email |
| conversion | 0/1 | Mua hàng trong 2 tuần sau email |
| spend | số | Số tiền chi trong 2 tuần sau email (đô la) |

Đặc trưng đo TRƯỚC can thiệp; visit, conversion, spend đo SAU.

## 6. Biến kết quả
- visit: 14,68%; conversion: 0,90%; spend = 0 ở 99,1% khách
- conversion trùng 100% với spend > 0 (cùng một sự kiện)
- spend khi > 0 (578 khách): trung bình 116,4; trung vị 80,8; độ lệch 1,76

## 7. Kiểm tra ngẫu nhiên hóa
|SMD| tối đa 0,016 (ngưỡng 0,1); mọi p-value > 0,35 (chi bình phương và Kruskal-Wallis). Các nhóm cân bằng trước can thiệp.

## 8. Hạn chế
- Conversion rất hiếm (đối chứng chỉ 122 đơn) nên tín hiệu uplift trên conversion yếu
- Can thiệp là email; chi phí ưu đãi (δ) không quan sát được, là tham số giả định
- Tổng thể là khách hiện hữu đã mua trong 12 tháng, không phải khách tiềm năng; kết quả không tự khái quát cho khách mới
- Một chiến dịch, một ngành, năm 2008: hạn chế khái quát
- Không có mã khách hàng

## 9. Xử lý trước khi dùng
- Gộp 3 giá trị `segment` thành `group` (men/women/control)
- Không loại dòng trùng; không chuẩn hóa ở bước EDA

## 10. Tái lập
Notebook: `lab/notebooks/01_hillstrom_eda.ipynb`; seed 42; kết quả: `lab/reports/figures/hillstrom_eda/` và `lab/reports/tables/hillstrom_eda/`.