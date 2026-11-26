# D-004: Kiến trúc ứng dụng web Angular và phân chia trách nhiệm hệ thống

Ngày: 26/11/2026 | Trạng thái: Đã chốt  
Liên quan: G-24.11.26 (Mục 5.1); Issue #5

## Bối cảnh
Để đánh giá artefact (RQ3) với các chuyên gia marketing và thương mại điện tử, hệ thống cần có giao diện thực tế gồm: (1) Cửa hàng trực tuyến phía khách hàng để trải nghiệm mua sắm, nhận mã và cấp quyền đồng ý dữ liệu cá nhân; (2) Dashboard quản trị dành cho người làm marketing mô phỏng phân bổ ngân sách, cấu hình chi phí và xem báo cáo hiệu quả gia tăng (uplift, Qini). Cần quyết định cấu trúc ứng dụng web để vừa thuận tiện demo, vừa phân tách rõ ràng trách nhiệm kỹ thuật và không làm phình to khối lượng công việc.

## Các phương án
1. **Tách thành hai ứng dụng web riêng biệt chạy trên 2 cổng (ports):**
   - *Ưu điểm:* Cô lập mã nguồn giữa hai đối tượng người dùng.
   - *Nhược điểm:* Phải cấu hình 2 dự án build, 2 luồng routing, trùng lặp thư viện UI, phức tạp hóa việc triển khai Docker và demo cho chuyên gia.
2. **Một ứng dụng Angular duy nhất chia làm hai khu vực chức năng bằng Lazy-Loaded Modules:**
   - *Ưu điểm:* Triển khai gọn nhẹ trên 1 domain/port; chia sẻ component dùng chung; đóng gói sạch sẽ; tối ưu tài nguyên; demo mượt mà.
   - *Nhược điểm:* Cần thiết lập route guards và quản lý state hợp lý.

## Quyết định
- **Xây dựng một ứng dụng Angular duy nhất với hai khu vực chức năng:**
  - **Khu vực Cửa hàng (`/store`):** Dành cho khách hàng (danh mục sản phẩm, chi tiết sản phẩm, giỏ hàng, đặt hàng, màn hình đồng ý thu thập dữ liệu cá nhân theo Luật 91/2025/QH15, nhận mã ưu đãi).
  - **Khu vực Quản trị (`/admin`):** Dành cho chuyên gia / marketer (tạo chiến dịch, cấu hình ngân sách và chi phí $c, \delta$, lựa chọn chính sách nhắm mục tiêu ngẫu nhiên / propensity / uplift / profit-driven uplift, xem dashboard trực quan đường cong Qini và lợi nhuận gia tăng kỳ vọng).
- **Phân tách bằng Lazy Loading và Route Guard:** Khu vực `/admin` được lazy load khi cần; Angular Route Guard chỉ để ẩn/hiện giao diện; phân quyền bảo mật thực tế được kiểm soát chặt chẽ ở backend API.
- **Tiết kiệm công sức (giữ tỷ trọng ≤ 30%):** Không xây dựng hệ thống quản lý sản phẩm / tồn kho (CRUD) phức tạp; toàn bộ danh mục sản phẩm và khách hàng mô phỏng được nạp tự động qua seed script.
- **Phân tách 3 dịch vụ trong Docker Compose theo trách nhiệm:**
  1. Frontend: Angular (Single Page Application).
  2. Business Backend: Node.js (NestJS hoặc Express) quản lý đơn hàng, giỏ hàng, xác thực và lưu log sự kiện.
  3. Model Serving Service: Python (FastAPI) phục vụ inference điểm propensity, uplift và tối ưu phân bổ ngân sách.

## Lý do và bằng chứng
- Hướng dẫn Mục 5.1 của Thầy nhấn mạnh: công nghệ là phương tiện, không nên phân mảnh ứng dụng. Chuyên gia đánh giá RQ3 sẽ tập trung trải nghiệm khu vực `/admin`, do đó cần tập trung nguồn lực UI/UX chất lượng cao vào dashboard mô phỏng chiến dịch.
- Việc dùng FastAPI làm dịch vụ mô hình riêng cho phép tái sử dụng 100% pipeline mã nguồn Python từ phòng thí nghiệm offline mà không phải viết lại thuật toán bằng JavaScript.

## Hệ quả
- Cấu trúc thư mục mã nguồn được phân định trong `app/`: `app/web/` (Angular), `app/api/` (Node.js API), `app/model-service/` (FastAPI).
- Chuẩn bị sẵn kịch bản seed data và kịch bản tác vụ đánh giá chuyên gia theo đúng kế hoạch Giai đoạn 3.
