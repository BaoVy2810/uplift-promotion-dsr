# D-001: Thiết kế so sánh cho bộ Hillstrom

Ngày: 26/11/2026 | Trạng thái: Đã chốt, chờ Thầy góp ý
Liên quan: G-24.11.26 (Mục 3.3, 6.3); notebook 01_hillstrom_eda; RQ1, RQ2

## Bối cảnh
Hillstrom có 3 nhóm (email nam, email nữ, không gửi) và 3 biến kết quả. Cần chốt cặp so sánh nhị phân và biến kết quả cho RQ1, RQ2 trước khi huấn luyện mô hình.

## Các phương án
1. Email nam vs đối chứng
2. Email nữ vs đối chứng
3. Gộp hai email vs đối chứng

## Quyết định
- Cặp chính: email nam vs đối chứng. Cặp phụ để kiểm tra khái quát: email nữ vs đối chứng.
- Không gộp hai email làm cặp chính.
- Biến kết quả huấn luyện và đánh giá chính: visit. Conversion và spend dùng cho phân tích lợi nhuận và độ nhạy.

## Lý do và bằng chứng (notebook 01_hillstrom_eda)
- Ngẫu nhiên hóa đạt: |SMD| tối đa 0,016; mọi p-value > 0,35
- ATE email nam: visit +7,66 điểm %, conversion +0,68 điểm %, spend +0,77. Email nữ: +4,52, +0,31, +0,42. Khoảng tin cậy 95% đều không chứa 0
- Email nam có hiệu ứng lớn hơn và nhiều sự kiện hơn (267 đơn mua so với 122 ở đối chứng, 189 ở email nữ)
- Hai email quảng bá hai danh mục khác nhau, hiệu ứng khác nhau; gộp là giả định cùng một can thiệp
- Conversion hiếm (đối chứng 122 đơn) nên ước lượng uplift trên conversion sẽ nhiễu; visit có nhiều sự kiện hơn (khoảng 2.260 ở đối chứng)

## Hệ quả và hạn chế
- Visit là biến thay thế, chưa phải doanh thu; mô hình lợi nhuận dùng conversion/spend với δ, c giả định
- Lựa chọn cặp chính dựa trên ATE toàn bộ dữ liệu, chưa chạy mô hình uplift nào. Để tránh chọn cặp theo kết quả tốt, cặp phụ (email nữ) vẫn được chạy đầy đủ và báo cáo
- Tập test sẽ cố định trong `docs/analysis_plan.md` trước khi huấn luyện
- Xem lại nếu mô hình trên visit không cho tín hiệu uplift

## Tham chiếu
G-24.11.26 (Mục 3.3, 6.3); Hevner et al. (2004) về thiết kế như quá trình tìm kiếm