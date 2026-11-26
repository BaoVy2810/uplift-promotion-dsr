# Kế hoạch phân tích thực nghiệm trước khi mô hình hóa (Pre-Analysis Plan)

**Dự án:** Cá nhân hóa khuyến mãi dựa trên mô hình Uplift trong Thương mại điện tử theo tiếp cận Khoa học thiết kế (DSR)  
**Tài liệu:** `docs/analysis_plan.md`  
**Ngày chốt:** 26/11/2026 | **Trạng thái:** Đã chốt trước khi huấn luyện mô hình  
**Căn cứ:** Ý kiến hướng dẫn của Thầy G-24.11.26 (Mục 3.2, 3.3, 6.3); Decision Log D-001; Notebook `01_hillstrom_eda.ipynb`

---

## 1. Mục tiêu và Nguyên tắc nghiêm ngặt (Preregistration Principle)

Theo chuẩn mực nghiên cứu thực nghiệm và suy luận nhân quả (Kohavi et al., 2020), kế hoạch phân tích này được xây dựng và **commit có dấu thời gian** lên Git repository trước khi tiến hành huấn luyện bất kỳ mô hình uplift nào.

Mục tiêu là:
1. Cố định các quyết định phân tích (cách chia dữ liệu, tham số chi phí, chỉ số đánh giá, mức ngân sách, chính sách so sánh) để loại bỏ thiên lệch chọn lọc sau thực nghiệm (post-hoc selection bias, p-hacking).
2. Trả lời trực tiếp **RQ1** và **RQ2** của khóa luận:
   - **RQ1:** Trong cùng ràng buộc ngân sách và ở các cấu trúc chi phí khác nhau, chính sách nhắm mục tiêu nào (ngẫu nhiên, propensity, uplift, uplift có tính lợi nhuận) tạo ra chuyển đổi và lợi nhuận gia tăng cao nhất?
   - **RQ2:** Các phương pháp ước lượng uplift khác nhau thế nào về hiệu quả và độ ổn định trên các bộ dữ liệu có cấu trúc khác nhau? Đặc trưng hành vi nào giải thích mức độ đáp ứng với khuyến mãi?

---

## 2. Thiết kế dữ liệu và Phân chia tập mẫu (Data Splitting Protocol)

### 2.1. Bộ dữ liệu áp dụng đầu tiên: Hillstrom (MineThatData Challenge)
- **Tổng quy mô:** 64.000 khách hàng.
- **Cặp so sánh nhị phân (theo D-001):**
  - **Cặp chính (Primary):** Nhóm nhận email hàng nam (`men`, $n = 21.307$) so với nhóm đối chứng không gửi email (`control`, $n = 21.306$). Tổng mẫu phân tích chính: $N = 42.613$.
  - **Cặp phụ kiểm tra độ khái quát (Robustness check):** Nhóm nhận email hàng nữ (`women`, $n = 21.387$) so với nhóm đối chứng (`control`, $n = 21.306$).
- **Biến kết quả:**
  - *Biến kết quả huấn luyện (Training Target):* `visit` (tín hiệu mạnh, tỷ lệ 14,7%, ATE = +7,66 điểm %).
  - *Biến kết quả đánh giá lợi nhuận (Economic Outcomes):* `conversion` (tỷ lệ 0,90%) và `spend` (doanh số thực tế trong 2 tuần).

### 2.2. Chiến lược chia dữ liệu (Data Partitioning)
- **Cố định hạt giống ngẫu nhiên:** `SEED = 42`.
- **Tỷ lệ phân chia:**
  - **Tập Huấn luyện (Train):** 60% (~25.568 mẫu).
  - **Tập Thẩm định (Validation):** 20% (~8.522 mẫu) - chỉ dùng để tinh chỉnh siêu tham số (hyperparameter tuning) và chọn mô hình.
  - **Tập Kiểm định (Test):** 20% (~8.523 mẫu) - **bị khóa hoàn toàn**, chỉ mở ra đánh giá một lần duy nhất khi đã chốt mô hình cuối cùng.
- **Phương pháp phân tầng (Stratification):** Phân tầng 2 chiều kết hợp theo `group` ($T \in \{0, 1\}$) và biến kết quả `visit` ($Y \in \{0, 1\}$) để bảo đảm tỷ lệ can thiệp và tỷ lệ chuyển đổi đồng nhất trên cả 3 tập.

---

## 3. Các mô hình và Phương pháp ước lượng

Nghiên cứu sẽ triển khai và so sánh các họ thuật toán sau:

### 3.1. Nhóm Baselines
1. **Random Targeting (Chính sách ngẫu nhiên):** Chọn khách hàng ngẫu nhiên theo tỷ lệ ngân sách. Đường kỳ vọng tuyến tính từ (0, 0) đến tổng hiệu ứng toàn quần thể.
2. **Propensity Targeting (Chính sách xác suất mua thông thường):** Huấn luyện mô hình phân loại dự đoán xác suất $P(Y=1 | X)$ chỉ trên dữ liệu quan sát (sử dụng LightGBM và Logistic Regression). Xếp hạng khách hàng theo điểm xác suất giảm dần.

### 3.2. Nhóm Uplift Modeling (Ước lượng CATE: $\tau(X) = E[Y|X, T=1] - E[Y|X, T=0]$)
1. **S-Learner (Single Model):** Huấn luyện 1 mô hình LightGBM duy nhất trên toàn bộ tập dữ liệu với đặc trưng $X$ và biến can thiệp $T$. Điểm uplift: $\hat{\tau}(X) = \hat{\mu}(X, 1) - \hat{\mu}(X, 0)$.
2. **T-Learner (Two Models):** Huấn luyện 2 mô hình độc lập: $\hat{\mu}_1(X)$ trên nhóm $T=1$ và $\hat{\mu}_0(X)$ trên nhóm $T=0$. Điểm uplift: $\hat{\tau}(X) = \hat{\mu}_1(X) - \hat{\mu}_0(X)$.
3. **X-Learner (Künzel et al., 2019):** Mô hình hai bước với hàm trọng số xu hướng (propensity score weighting), đặc biệt hiệu quả khi có sự chênh lệch quy mô nhóm hoặc tín hiệu phân tán.
4. **Class Transformation (Lai's Generalized Method / Jaskowski & Jaroszewicz):** Biến đổi biến kết quả nhị phân $Z_i = Y_i T_i + (1 - Y_i)(1 - T_i)$. Khi $P(T=1) = 0.5$, $E[2Z_i - 1 | X_i] = \tau(X_i)$. Huấn luyện mô hình phân loại dự đoán $Z$.
5. **Causal Forest (Wager & Athey, 2018):** Sử dụng rừng ngẫu nhiên nhân quả (thông qua thư viện EconML / CausalML) để ước lượng phi tham số CATE kèm khoảng tin cậy tiệm cận.

---

## 4. Mô hình Kinh tế và Bốn Chính sách Nhắm mục tiêu (Targeting Policies)

### 4.1. Cấu trúc Mô hình Lợi nhuận (Profit Model)
Kế thừa khung lý thuyết của Haupt & Lessmann (2022) và Verbeke et al. (2023), phân định rõ hai loại chi phí:
- $c$: Chi phí tiếp cận trên mỗi khách hàng được nhắm tới (chi phí gửi email, SMS, hiển thị quảng cáo). Phát sinh cho mọi khách được chọn, bất kể họ có mua hay không.
- $\delta$: Chi phí ưu đãi trên mỗi đơn hàng thành công có áp dụng khuyến mãi (tiền giảm giá, chiết khấu, miễn phí vận chuyển). Phát sinh khi và chỉ khi khách mua hàng dưới điều kiện can thiệp.
- $m$: Biên lợi nhuận gộp trung bình của một đơn hàng (trước khi trừ ưu đãi $\delta$).

Lợi nhuận kỳ vọng khi gửi khuyến mãi cho khách hàng $i$:
$$E[\Pi | T=1, X_i] = p_T(X_i) \cdot (m - \delta) - c$$

Lợi nhuận kỳ vọng khi không gửi khuyến mãi (đối chứng):
$$E[\Pi | T=0, X_i] = p_C(X_i) \cdot m$$

**Lợi nhuận gia tăng kỳ vọng khi nhắm mục tiêu khách hàng $i$ ($\Delta \Pi(i)$):**
$$\Delta \Pi(i) = E[\Pi | T=1, X_i] - E[\Pi | T=0, X_i] = \left[p_T(X_i) - p_C(X_i)\right] \cdot m - \delta \cdot p_T(X_i) - c$$
$$\Delta \Pi(i) = \tau(i) \cdot m - \delta \cdot p_T(X_i) - c$$

Trong đó:
- $\tau(i) = p_T(X_i) - p_C(X_i)$ là điểm uplift của khách hàng $i$.
- $p_T(X_i)$ là xác suất mua hàng ước lượng khi nhận can thiệp.

> **Ý nghĩa khoa học cốt lõi:**
> Công thức này giải thích toán học vì sao mô hình Propensity thất bại và gây lỗ: Nhóm khách hàng *Sure Things* có $p_T(i)$ rất cao nhưng $\tau(i) \approx 0$, dẫn đến phần chi phí $-\delta \cdot p_T(i)$ triệt tiêu toàn bộ lợi nhuận. Chỉ có khách hàng có uplift $\tau(i)$ đủ lớn để bù đắp chi phí ưu đãi $\delta \cdot p_T(i)$ và chi phí tiếp cận $c$ mới đem lại giá trị thặng dư $(\Delta \Pi(i) > 0)$.

### 4.2. Bốn Chính sách Nhắm mục tiêu So sánh
1. **Policy 1 - Ngẫu nhiên (Random):** Xếp ngẫu nhiên danh sách khách hàng.
2. **Policy 2 - Thiên hướng mua (Propensity-based):** Xếp hạng khách hàng giảm dần theo xác suất mua $p_T(X_i)$.
3. **Policy 3 - Hiệu ứng gia tăng (Conventional Uplift-based):** Xếp hạng khách hàng giảm dần theo điểm uplift $\hat{\tau}(X_i)$.
4. **Policy 4 - Uplift tối ưu lợi nhuận (Profit-driven Uplift):** Xếp hạng khách hàng giảm dần theo lợi nhuận gia tăng kỳ vọng $\Delta \hat{\Pi}(i)$. Chỉ kích hoạt can thiệp cho khách hàng có $\Delta \hat{\Pi}(i) > 0$.

### 4.3. Cấu hình Tham số và Phân tích Độ nhạy (Sensitivity Analysis)
Với bộ dữ liệu Hillstrom, vì can thiệp thực tế là email (chi phí $\delta$ là giả định), nghiên cứu thiết lập ma trận phân tích độ nhạy với các tham số:
- Biên lợi nhuận chuẩn hóa: $m = 10.0$ (hoặc giá trị đơn hàng trung bình từ biến `spend`).
- Chi phí tiếp cận $c \in \{0.01, 0.05, 0.1, 0.5\}$ (từ chi phí email cực thấp đến SMS/quảng cáo).
- Chi phí ưu đãi $\delta \in \{0.0, 1.0, 2.0, 3.0, 5.0\}$ (tương ứng từ 0% đến 50% biên lợi nhuận $m$).
- Các mức ngân sách / tỷ lệ tiếp cận (Cutoff $k$): 5%, 10%, 20%, 30%, 40%, 50%, 100%.

---

## 5. Chỉ số Đánh giá Thực nghiệm (Evaluation Metrics)

1. **Đường cong Qini và Hệ số Qini (Qini curve & normalized Qini score $Q$):**
   $$Qini(k) = Y_{T=1}(k) - Y_{T=0}(k) \cdot \frac{N_{T=1}(k)}{N_{T=0}(k)}$$
   Đo lường số lượng chuyển đổi gia tăng tích lũy theo từng phân vị khách hàng $k$.
2. **Diện tích dưới đường cong Uplift (AUUC - Area Under the Uplift Curve):** Đo lường năng lực phân tách tổng thể của mô hình uplift so với đường ngẫu nhiên.
3. **Uplift tại phân vị cố định (Uplift@k%):** Hiệu ứng gia tăng tuyệt đối khi chọn top $k\%$ ($k \in \{10\%, 20\%, 30\%\}$).
4. **Lợi nhuận gia tăng thực tế tích lũy (Cumulative Incremental Profit):**
   $$\Pi_{cum}(k) = \sum_{i \in \text{Top } k} \left[ \tau(i) \cdot m - \delta \cdot p_T(i) - c \right]$$
5. **Độ ổn định và Khoảng tin cậy:** Tính toán khoảng tin cậy 95% qua phương pháp Bootstrap (1.000 lần lặp) trên tập test độc lập để kiểm định ý nghĩa thống kê giữa các chính sách.

---

## 6. Giải thích Mô hình và Suy luận Đặc trưng (RQ2 - Explainability)

- Sử dụng phương pháp **SHAP (SHapley Additive exPlanations)** trên mô hình uplift tốt nhất (S-Learner / T-Learner / Causal Forest).
- Phân tích đóng góp của các đặc trưng lịch sử mua sắm (`recency`, `history`, `channel`, `mens`, `womens`, `newbie`, `zip_code`) đối với mức độ nhạy cảm của khách hàng với khuyến mãi.
- Vẽ biểu đồ SHAP summary plot và partial dependence plot để rút ra phát hiện quản trị cho nhà bán lẻ.

---

## 7. Quy trình Tái lập (Reproducibility Protocol)

1. Mọi tham số siêu cấp, hạt giống ngẫu nhiên, cấu hình chi phí được lưu trữ tại `lab/configs/`.
2. Mã nguồn tái sử dụng được đặt tại `lab/src/uplift_lab/` và có unit test tại `lab/tests/`.
3. Nhật ký thử nghiệm tự động ghi lại phiên bản qua MLflow (hoặc log CSV có timestamp).
4. Toàn bộ notebook phân tích phải thực hiện thành công quy trình **Restart & Run All** mà không phát sinh lỗi trước khi commit.
