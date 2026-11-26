# D-003: Chọn hệ quản trị CSDL cho website và 4 điều kiện bảo toàn dữ liệu nghiên cứu

Ngày: 26/11/2026 | Trạng thái: Đã chốt  
Liên quan: G-24.11.26 (Mục 5.2); Issue #4

## Bối cảnh
Website bán hàng trong đề tài đóng vai trò là artefact và môi trường thực nghiệm trực tuyến (RQ3). Hệ thống cần lưu trữ dữ liệu sự kiện người dùng (click, view, add_to_cart), thông tin đồng ý dữ liệu cá nhân (consents), đơn hàng, và đặc biệt là dữ liệu phân bổ chiến dịch (assignments: ai nhận mã, ai thuộc nhóm đối chứng holdout, theo phiên bản mô hình nào). Dữ liệu phân nhóm chiến dịch là bằng chứng thực nghiệm của khóa luận, đòi hỏi tính toàn vẹn, kiểm tra lại được và chống ghi đè. Cần chọn hệ quản trị CSDL vừa tận dụng được kỹ năng của sinh viên vừa đáp ứng tiêu chuẩn nghiên cứu khoa học.

## Các phương án
1. **MongoDB:**
   - *Ưu điểm:* Sinh viên đã thành thạo; cấu trúc tài liệu BSON linh hoạt, rất phù hợp với dữ liệu sự kiện (events) có thuộc tính biến đổi tùy loại hành vi; phát triển nhanh.
   - *Nhược điểm:* Mặc định không ràng buộc quan hệ chặt chẽ; multi-document transaction cần cấu hình replica set; nếu không kiểm soát sẽ gây sai lệch dữ liệu phân nhóm.
2. **PostgreSQL:**
   - *Ưu điểm:* Cấu trúc quan hệ chuẩn mực (ACID mặc định); bảo đảm tính toàn vẹn dữ liệu phân nhóm; hỗ trợ JSONB cho sự kiện linh hoạt.
   - *Nhược điểm:* Đòi hỏi thời gian thiết kế migration và ORM lớn hơn; tăng tải công việc phát triển web ngoài ngưỡng 30% công sức.

## Quyết định
- **Giữ MongoDB** làm CSDL cho website artefact để tối ưu thời gian phát triển cho nghiên cứu, nhưng **bắt buộc tuân thủ 4 điều kiện kiểm soát tính toàn vẹn** do Thầy chỉ định:
  1. **Mỗi khách chỉ được phân nhóm một lần trong một chiến dịch:** Tạo unique compound index `{ campaign_id: 1, customer_id: 1 }` trên collection `assignments`.
  2. **Dữ liệu đúng cấu trúc:** Bật schema validation (`$jsonSchema`) với `validationAction: "error"` cho 4 collection trọng yếu: `assignments`, `campaigns`, `coupons`, `consents`. Bản ghi sai định dạng sẽ bị từ chối ở tầng CSDL.
  3. **Phát mã và đặt hàng nhất quán:** Cấu hình MongoDB dạng Single-Node Replica Set trong Docker Compose để hỗ trợ Multi-Document Transactions.
  4. **Phân tích độc lập bằng Python:** Dữ liệu nghiên cứu offline không nằm trong CSDL website. Viết script xuất dữ liệu assignments/events/orders sang định dạng Parquet (dùng pymongo kết hợp DuckDB/Polars) để phân tích bằng pipeline Python, không dồn logic phân tích phức tạp vào MongoDB aggregation.
- Nguyên tắc ghi dữ liệu: Các collection `assignments`, `events` và `consents` là **Append-only** (chỉ ghi thêm, không cập nhật hay xóa đè).

## Lý do và bằng chứng
- Đáp ứng trọn vẹn yêu cầu phương pháp luận: dữ liệu phân nhóm và nhóm đối chứng (holdout) là căn cứ khoa học đo lường hiệu quả gia tăng (Kohavi et al., 2020), do đó 4 điều kiện trên loại bỏ rủi ro gian lận hoặc sai lệch dữ liệu.
- Giữ được tỷ trọng phát triển phần mềm trong giới hạn ≤ 30% tổng công sức khóa luận, dành 70% còn lại cho phương pháp uplift, phân tích thực nghiệm và viết báo cáo.

## Hệ quả
- File `docker-compose.yml` sẽ khởi tạo MongoDB với tham số `--replSet rs0` và có script tự động `rs.initiate()`.
- Pipeline dữ liệu phân tích sẽ duy trì mã nguồn trích xuất Parquet trong `lab/src/uplift_lab/data.py`.
