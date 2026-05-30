# Đánh giá Kết quả PageRank — Dataset ca-GrQc

**Dataset:** Collaboration Network — arXiv General Relativity & Quantum Cosmology (Stanford SNAP)  
**Quy mô:** 5,241 nút · 28,968 cạnh · **0 dangling nodes** · out/in-degree tối đa bằng nhau (81)  
**Thuật toán:** Sparse Power Iteration, α = 0.85, hội tụ sau **118 vòng lặp** (0.414s)

> **Đặc điểm quan trọng:** ca-GrQc là mạng cộng tác khoa học (undirected graph được biểu diễn thành directed bằng cách thêm cả hai chiều cho mỗi cạnh). Điều này tạo ra tính chất **in-degree = out-degree** cho mọi nút — khác biệt căn bản với hai dataset kia.

---

## 1. Phân phối PageRank Score (Biểu đồ trên trái)

### Quan sát

Đường cong log-scale có hình dạng **khác biệt rõ rệt** so với Gnutella04 và wiki-Vote:

- **Không dốc đứng ngay từ đầu** — giảm tương đối đều từ hạng 1 đến ~3,000.
- **Vùng giữa (hạng 1,000–3,500):** đường cong có độ dốc đều, gần tuyến tính trên log-scale.
- **Đuôi cuối (hạng 4,000+):** có một "vách dốc" đột ngột — nhiều nút cùng nhau có score rất thấp gần bằng 0.
- **Score top 1 (≈ 0.00144) thấp hơn wiki-Vote (0.00461)** dù ít nút hơn — cho thấy rank được phân phối đều hơn.

### Nhận xét — Mạng cộng tác có phân phối "mượt mà" hơn

Do tính chất **symmetric** của mạng cộng tác:

- Rank "chảy" hai chiều qua mỗi cạnh → không có nút nào tích lũy rank từ một phía mà không đóng góp lại.
- Không hình thành super-hub kiểu web (trang thu hút liên kết vào mà không liên kết ra).
- **Cộng đồng nghiên cứu** (research community / clique) tạo ra các cụm nút score đồng đều trong cluster, dẫn đến đường cong mượt mà.
- Vách dốc ở đuôi tương ứng với các nhà khoa học cô lập (chỉ có 1–2 cộng tác), bị cut khỏi component lớn.

---

## 2. Top 20 Nút (Biểu đồ trên phải)

### Quan sát

| Hạng | Nút | Score |
|------|-----|-------|
| 1 | P02773 | 0.00144317 |
| 2 | P02713 | 0.00134123 |
| 3 | P02725 | 0.00130603 |
| 4 | P04281 | 0.00117802 |
| 5 | P01934 | 0.00116955 |
| … | … | … |
| 20 | P01489 | 0.00091651 |

Chênh lệch top 1 / top 20 = **1.57×** — thấp tương đương Gnutella04, cho thấy phân phối khá đồng đều trong nhóm dẫn đầu.

### Nhận xét — Top trang là các nhà khoa học "cầu nối"

Trong mạng cộng tác khoa học, nút có PageRank cao không chỉ là người "nổi tiếng" (nhiều liên kết) mà còn là người **kết nối nhiều nhóm nghiên cứu khác nhau**:

- P02773 (hạng 1) có thể là nhà khoa học có in-degree = out-degree = 81 và nằm ở trung tâm nhiều cluster.
- Trong mạng symmetric: **PageRank ≈ Degree Centrality** — nút nào có nhiều cộng tác nhất thường đứng đầu.
- Tuy nhiên có ngoại lệ: P04281 (hạng 4) có in-degree = 81 tương đương P02773, nhưng rank thấp hơn — do P02773 kết nối với các nút có rank cao hơn (tính chất eigenvector centrality).

---

## 3. Ảnh hưởng của Damping Factor α (Biểu đồ dưới trái)

### Quan sát — Hiện tượng đặc biệt: đường cắt nhau

5 đường màu cho thấy **sự không ổn định rõ ràng** khi α tăng cao:

- **P04281 (cam/vàng):** bắt đầu thấp (α=0.5) nhưng tăng mạnh, **cắt qua các đường khác** ở α ≈ 0.85–0.90, và vươn lên **cao nhất ở α = 0.95**.
- **P02773 (đỏ):** dẫn đầu ở α thấp và trung bình, nhưng bị P04281 vượt qua ở α cao.
- **P02725 (xanh lá) và P02713 (xanh dương):** tăng đều nhưng không giữ được khoảng cách.
- Kết quả: **Trang đứng đầu thay đổi từ P02773 → P04232 khi α = 0.95**.

| α | Trang đứng đầu | Score | Vòng lặp | ρ (Spearman) |
|---|---|---|---|---|
| 0.50 | P02773 | 0.001131 | 28 | 0.9758 |
| 0.65 | P02773 | 0.001307 | 45 | 0.9872 |
| 0.75 | P02773 | 0.001394 | 67 | 0.9942 |
| 0.85 | P02773 | 0.001443 | **118** | 1.0000 |
| 0.90 | P02773 | 0.001442 | **182** | 0.9962 |
| 0.95 | **P04232** | 0.001586 | **374** | 0.9877 |

**Nhận xét quan trọng:**

1. **Số vòng lặp tăng đột biến khi α tăng** (28 → 374 vòng): mạng symmetric có eigenvalue thứ hai của P (λ₂) gần 1 hơn, khiến tốc độ hội tụ |α·λ₂| chậm hơn nhiều khi α lớn.

2. **P02773 score "đỉnh" tại α=0.85** rồi giảm nhẹ ở α=0.90 — hiện tượng bất thường: với mạng symmetric, λ₂ ≈ 1 làm phân phối rank bị kéo về eigenvector thứ hai khi α → 1, dẫn đến **dao động hoặc xáo trộn thứ hạng ở α rất cao**.

3. **Top-10 overlap ở α=0.95 chỉ còn 6/10** — thấp nhất trong ba dataset, minh chứng cho sự nhạy cảm hơn với α trong mạng cộng tác.

---

## 4. Ma trận Tương quan Spearman (Biểu đồ dưới phải)

### Quan sát

Ma trận có màu **không đồng nhất** — có ô màu vàng/xanh nhạt ở cột/hàng α=0.95 và α=0.50:

| | 0.50 | 0.65 | 0.75 | 0.85 | 0.90 | 0.95 |
|--|--|--|--|--|--|--|
| **0.50** | 1.000 | 0.985 | 0.975 | 0.976 | 0.965 | **0.946** |
| **0.65** | 0.985 | 1.000 | 0.995 | 0.987 | 0.979 | 0.963 |
| **0.75** | 0.975 | 0.995 | 1.000 | 0.994 | 0.988 | 0.975 |
| **0.85** | 0.976 | 0.987 | 0.994 | 1.000 | 0.996 | 0.984 |
| **0.90** | 0.965 | 0.979 | 0.988 | 0.996 | 1.000 | **0.994** |
| **0.95** | **0.946** | 0.963 | 0.975 | 0.984 | 0.994 | 1.000 |

**Tương quan thấp nhất: ρ = 0.946** (cặp α=0.50 và α=0.95) — thấp hơn đáng kể so với wiki-Vote (0.992) và Gnutella04 (0.993).

### Nhận xét — Tại sao ca-GrQc nhạy cảm hơn với α?

Nguyên nhân cốt lõi nằm ở **cấu trúc spectral** của mạng:

- **Mạng cộng tác symmetric → eigenvalues của ma trận P thực và gần 1**: Với undirected graph, nhiều eigenvalue có thể xấp xỉ 1, làm |α·λ₂| ≈ α → hội tụ chậm và nhạy cảm với α.
- **Community structure mạnh (clique nội bộ):** Mỗi research group là một clique gần đầy đủ. Khi α thay đổi, trọng số giữa các community thay đổi, có thể đưa nút khác nhau lên đỉnh.
- **0 dangling nodes:** Không có cơ chế "làm mượt" tự nhiên qua dangling teleportation như Gnutella04.

---

## 5. So sánh Biến thể PageRank

| Biến thể | Tương quan Spearman với Standard |
|---|---|
| Standard | 1.0000 |
| Weighted | 0.9541 |
| Topic-Sensitive | 0.5369 |
| **Personalized** | **0.1691** |

**Personalized PR chỉ tương quan 0.169 với Standard** — cực kỳ khác biệt, thấp nhất trong cả ba dataset. Lý do:

- **Community structure cô lập**: seed (top-5 in-degree nodes) thuộc về một vài cluster khoa học. Khi teleportation chỉ về seed, toàn bộ rank tập trung vào cluster đó và cô lập hoàn toàn với phần còn lại của mạng.
- **Hiệu ứng "bong bóng community"**: Kết quả PPR hoàn toàn khác Standard vì trong mạng cộng tác, một nhà khoa học ngoài community của seed gần như không được PPR "nhìn đến".

---

## 6. So sánh ba dataset thực

| Tiêu chí | wiki-Vote | p2p-Gnutella04 | **ca-GrQc** |
|---|---|---|---|
| Loại đồ thị | Có hướng (voting) | Có hướng (P2P) | Vô hướng → có hướng |
| Nút / Cạnh | 7,115 / 103,689 | 10,876 / 39,994 | 5,241 / 28,968 |
| Dangling nodes | 14.1% | 54.6% | **0%** |
| In-degree tối đa | 457 | 72 | **81 = Out-degree tối đa** |
| Vòng lặp (α=0.85) | 29 | 18 | **118** |
| ρ_min Spearman (α) | 0.992 | 0.993 | **0.946** |
| Standard vs PPR | 0.973 | 0.733 | **0.169** |
| Top-10 overlap (α=0.95) | 10/10 | 9/10 | **6/10** |

**Kết luận:** ca-GrQc là dataset **khó hội tụ nhất** và **nhạy cảm nhất với α** trong ba dataset. Nguyên nhân là do tính chất symmetric của mạng cộng tác tạo ra eigenvalue thứ hai gần 1. Đây là ví dụ điển hình cho thấy **PageRank được thiết kế tối ưu cho đồ thị web có hướng bất đối xứng** — khi áp dụng cho mạng cộng tác symmetric, các tham số như α cần được hiệu chỉnh cẩn thận hơn.
