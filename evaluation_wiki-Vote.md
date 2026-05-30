# Đánh giá Kết quả PageRank — Dataset wiki-Vote

**Dataset:** Wikipedia Voting Network (Stanford SNAP)  
**Quy mô:** 7,115 nút · 103,689 cạnh có hướng · 1,005 dangling nodes  
**Thuật toán:** Sparse Power Iteration, α = 0.85, hội tụ sau 29 vòng lặp

---

## 1. Phân phối PageRank Score (Biểu đồ trên trái)

### Quan sát

Trục Y (log scale) cho thấy đường cong giảm cực dốc ngay từ đầu, sau đó dẹt dần về cuối. Cụ thể:

- **Top 1 trang (P03649):** score ≈ 0.0046 — cao hơn trang hạng 20 khoảng **2.5 lần**
- **Top ~50 trang:** score ≥ 10⁻³, chiếm phần lớn tổng rank
- **Hạng 1,000 trở đi:** đường cong phẳng lại ở vùng 10⁻⁴, hàng nghìn trang có score gần bằng nhau

### Nhận xét — Phân phối Power-Law

Dạng đường cong trên log-scale tương đương **phân phối power-law (long-tail)**:

$$\pi(k) \sim k^{-\gamma}$$

Đây là đặc trưng điển hình của đồ thị web thực tế:
- **Một số ít trang "hub" chiếm ưu thế** — nhận rất nhiều liên kết vào từ khắp nơi.
- **Đại đa số trang có rank thấp** — ít được liên kết đến, điểm gần đồng đều với nền.
- Hiện tượng này phản ánh nguyên lý **"rich get richer"** (Barabási–Albert): trang đã nổi tiếng càng dễ nhận thêm liên kết mới.

Trong wiki-Vote, cơ chế này ứng với: **người dùng Wikipedia có uy tín càng cao thì càng được nhiều người khác bỏ phiếu tín nhiệm**, tạo ra cấu trúc bất đối xứng rõ rệt.

---

## 2. Top 20 Trang (Biểu đồ trên phải)

### Quan sát

| Hạng | Trang | Score |
|------|-------|-------|
| 1 | P03649 | 0.00461 |
| 2 | P00012 | 0.00368 |
| 3 | P05806 | 0.00359 |
| 4 | P02410 | 0.00328 |
| 5 | P02204 | 0.00261 |
| … | … | … |
| 20 | P03064 | 0.00178 |

Các thanh giảm dần đều (gần tuyến tính) từ hạng 1 đến hạng 20, cho thấy **không có cách biệt đột ngột** giữa các trang trong nhóm top — đây là nhóm "authority" thuần nhất.

### Nhận xét — Cấu trúc liên kết quyết định thứ hạng

- **P03649** dẫn đầu với in-degree cao nhất (457 liên kết vào) — tương ứng một người dùng Wikipedia nhận được nhiều phiếu tín nhiệm nhất.
- Nhóm top-5 chiếm tỉ lệ score cao hơn hẳn so với phần còn lại, phản ánh **cấu trúc hub tập trung** của mạng bỏ phiếu.
- Không có trang nào vượt trội cô lập — top-20 đều thuộc vùng "high-authority" liên kết chéo lẫn nhau.

---

## 3. Ảnh hưởng của Damping Factor α (Biểu đồ dưới trái)

### Quan sát

5 đường màu tương ứng top-5 trang, α tăng từ 0.5 đến 0.95:

- **Tất cả 5 đường đều tăng đơn điệu** khi α tăng → α lớn hơn làm score của trang quan trọng cao hơn.
- **P03649 (đỏ)** luôn cao nhất và có độ dốc lớn nhất → đây là trang hưởng lợi nhiều nhất từ cấu trúc liên kết.
- **Khoảng cách giữa P03649 và P02204 (tím)** rộng ra khi α tăng → α lớn **khuếch đại bất bình đẳng** giữa hub và trang thường.
- Ở α = 0.50: score từ 0.0017 đến 0.0035 (chênh lệch hẹp).
- Ở α = 0.95: score từ 0.0019 đến 0.0047 (chênh lệch rộng hơn ~50%).

### Nhận xét — Vai trò của α

| α | Ý nghĩa | Hệ quả |
|---|---------|--------|
| Thấp (0.5) | Random jump chiếm 50% | Score đồng đều, hội tụ nhanh (17 vòng), phân biệt kém |
| Trung bình (0.85) | Cân bằng link-following và teleport | Kết quả sát với tầm quan trọng thực, 29 vòng lặp |
| Cao (0.95) | Link structure chiếm 95% | Hub được khuếch đại tối đa, hội tụ chậm hơn (35 vòng) |

**Thứ tự xếp hạng top-5 không thay đổi** trên toàn dải α — cho thấy cấu trúc đồ thị, chứ không phải α, là yếu tố quyết định chính.

---

## 4. Ma trận Tương quan Spearman giữa các α (Biểu đồ dưới phải)

### Quan sát

Ma trận 6×6 ứng với α ∈ {0.50, 0.65, 0.75, 0.85, 0.90, 0.95}:

| | 0.50 | 0.65 | 0.75 | 0.85 | 0.90 | 0.95 |
|--|--|--|--|--|--|--|
| **0.50** | 1.000 | 0.996 | 0.998 | 0.995 | 0.995 | 0.992 |
| **0.65** | 0.996 | 1.000 | 0.998 | 0.997 | 0.996 | 0.991 |
| **0.75** | 0.998 | 0.998 | 1.000 | 0.998 | 0.998 | 0.993 |
| **0.85** | 0.995 | 0.997 | 0.998 | 1.000 | 0.999 | 0.992 |
| **0.90** | 0.995 | 0.996 | 0.998 | 0.999 | 1.000 | 0.992 |
| **0.95** | 0.992 | 0.991 | 0.993 | 0.992 | 0.992 | 1.000 |

Toàn bộ ma trận màu xanh đậm — tương quan thấp nhất là **ρ = 0.991** (cặp α=0.65 và α=0.95).

### Nhận xét — Độ bền của xếp hạng

Kết quả cực kỳ rõ ràng:

1. **Xếp hạng PageRank cực kỳ bền vững** với sự thay đổi của α trên dải [0.50, 0.95].
2. Tương quan gần bằng 1 chứng tỏ **cấu trúc in-link của đồ thị là nhân tố chi phối**, không phải lựa chọn α.
3. Cặp α xa nhau nhất (0.50 và 0.95) vẫn đạt ρ = 0.992 — **sai khác xếp hạng rất nhỏ**.
4. Với dữ liệu thực (wiki-Vote), giá trị α trong khoảng **0.75 – 0.90 là vùng an toàn** cho kết quả ổn định nhất (tương quan lẫn nhau ≥ 0.998).

---

## 5. Tổng hợp — So sánh Synthetic vs. wiki-Vote

| Tiêu chí | Synthetic (150 trang) | wiki-Vote (7,115 trang) |
|---|---|---|
| Phân phối score | Power-law nhẹ | Power-law mạnh hơn |
| Score trang #1 | 0.0243 | 0.0046 |
| Chênh lệch #1 vs #20 | ~2.7× | ~2.5× |
| Số vòng lặp (α=0.85) | 31 | 29 |
| Ổn định α | ρ ≥ 0.986 | ρ ≥ 0.992 |
| Dangling nodes | 0 | 1,005 (14.1%) |

Đồ thị thực có **ρ cao hơn** đồ thị tự sinh — cho thấy mạng wiki-Vote có cấu trúc hub-authority mạnh và nhất quán hơn, ít bị ảnh hưởng bởi α.

---

## 6. Kết luận

**Về dataset wiki-Vote:**
- Mạng bỏ phiếu Wikipedia thể hiện đầy đủ đặc trưng của đồ thị web thực: phân phối power-law, hub chiếm ưu thế, phần lớn nút có rank thấp.
- P03649 là người dùng có ảnh hưởng lớn nhất, được cộng đồng tín nhiệm rộng rãi nhất.

**Về thuật toán PageRank:**
- Power Iteration hội tụ chỉ sau **29 vòng** trên 7,115 nút — xác nhận hiệu quả của Sparse Implementation O(|E|).
- Google matrix G = αP + (1-α)(1/n)ee^T đảm bảo hội tụ duy nhất theo định lý Perron-Frobenius, ngay cả với 1,005 dangling nodes.
- α = 0.85 là lựa chọn cân bằng tối ưu giữa tốc độ hội tụ và chất lượng phân biệt trang.

**Về ý nghĩa thực tiễn:**
- Xếp hạng PageRank có thể được **tin cậy độc lập với lựa chọn α** — tương quan Spearman > 0.99 trên toàn dải α ∈ [0.5, 0.95].
- Cấu trúc liên kết (ai vote cho ai) là nhân tố quyết định thứ hạng, không phải tham số mô hình.
