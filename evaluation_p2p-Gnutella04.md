# Đánh giá Kết quả PageRank — Dataset p2p-Gnutella04

**Dataset:** Gnutella Peer-to-Peer File Sharing Network (Stanford SNAP)  
**Quy mô:** 10,876 nút · 39,994 cạnh có hướng · **5,941 dangling nodes (54.6%)**  
**Thuật toán:** Sparse Power Iteration, α = 0.85, hội tụ sau **18 vòng lặp** (0.088s)

---

## 1. Phân phối PageRank Score (Biểu đồ trên trái)

### Quan sát

Đường cong log-scale giảm rất dốc trong 500 hạng đầu, sau đó kéo thành đuôi dài và phẳng kéo đến tận hạng 10,000+. Cụ thể:

- **Top 1 (P01056):** score ≈ 0.00067
- **Top 20:** score ≈ 0.00042 — chênh lệch với top 1 chỉ khoảng **1.6×**
- **Phần đuôi (hạng 2,000 trở đi):** đường cong gần như nằm ngang ở mức ~10⁻⁴

### Nhận xét — Phân phối "đuôi rất dài"

So với wiki-Vote, đường cong của p2p-Gnutella04 **ít dốc hơn ở đỉnh** nhưng **đuôi dài hơn nhiều** (10,876 nút). Điều này phản ánh bản chất mạng P2P:

- **Không có super-hub rõ ràng** — không có nút nào vượt trội hoàn toàn như Wikipedia.
- **Phân phối phẳng hơn:** mạng Gnutella được thiết kế để phân tán đều, không tập trung vào một máy chủ trung tâm.
- **54.6% dangling nodes** — hơn nửa số nút không có liên kết ra (peer chỉ nhận, không chuyển tiếp). Cơ chế teleportation đóng vai trò quan trọng hơn để duy trì tính irreducible của G.

---

## 2. Top 20 Nút (Biểu đồ trên phải)

### Quan sát

| Hạng | Nút | Score |
|------|-----|-------|
| 1 | P01056 | 0.00067072 |
| 2 | P01054 | 0.00066316 |
| 3 | P01536 | 0.00054976 |
| 4 | P00171 | 0.00054385 |
| 5 | P00453 | 0.00052389 |
| … | … | … |
| 20 | P00987 | 0.00041863 |

Đặc điểm nổi bật: **P01056 và P01054 gần như bằng nhau** (chênh < 1.2%). Từ hạng 3 trở đi, điểm giảm đều và mượt mà đến hạng 20.

### Nhận xét — Cấu trúc phẳng, không có hub áp đảo

- **Chênh lệch hạng 1 vs hạng 20 chỉ là ~1.6×** — thấp nhất trong ba dataset. Trong wiki-Vote, tỉ lệ này là 2.5×.
- Điều này phản ánh **mạng P2P có cấu trúc phi tập trung**: các peer (nút) được thiết kế để tương đương nhau, không ai giữ vai trò "server" tuyệt đối.
- **In-degree lớn nhất chỉ là 72** — rất thấp so với wiki-Vote (457). Đây là đặc trưng của mạng P2P thế hệ đầu (Gnutella): giới hạn kết nối mỗi peer để tránh tắc nghẽn.

---

## 3. Ảnh hưởng của Damping Factor α (Biểu đồ dưới trái)

### Quan sát

5 đường màu tương ứng top-5 nút, α từ 0.5 đến 0.95:

- **Tất cả 5 đường gần như song song và có cùng độ dốc** — không có đường nào vọt lên hay tụt xuống mạnh.
- Khoảng cách giữa 5 đường **không đổi đáng kể** khi α tăng.
- Ở α = 0.50: score ≈ 0.00042–0.00043 (rất sát nhau).
- Ở α = 0.95: score ≈ 0.00063–0.00075 (vẫn sát nhau, tỉ lệ tương tự).
- **Không có đường nào cắt nhau** — thứ tự xếp hạng ổn định hoàn toàn.

### Nhận xét — Xếp hạng cực kỳ ổn định

| α | Trang đầu | Score | Iter | ρ (Spearman) |
|---|-----------|-------|------|------|
| 0.50 | P01054 | 0.00043 | 13 | 0.9938 |
| 0.65 | P01054 | 0.00053 | 15 | 0.9978 |
| 0.75 | P01054 | 0.00060 | 16 | 0.9994 |
| 0.85 | P01056 | 0.00067 | 18 | 1.0000 |
| 0.90 | P01056 | 0.00071 | 18 | 0.9999 |
| 0.95 | P01056 | 0.00075 | 19 | 0.9994 |

Lưu ý: **P01054 và P01056 hoán đổi vị trí số 1 khi α vượt qua ngưỡng ~0.80** — minh chứng trực quan rằng α có thể tác động đến thứ hạng ở vùng score rất sát nhau, dù tương quan tổng thể vẫn rất cao (ρ > 0.993).

---

## 4. Ma trận Tương quan Spearman (Biểu đồ dưới phải)

### Quan sát

| | 0.50 | 0.65 | 0.75 | 0.85 | 0.90 | 0.95 |
|--|--|--|--|--|--|--|
| **0.50** | 1.000 | 0.994 | 0.997 | 0.994 | 0.993 | 0.993 |
| **0.65** | 0.994 | 1.000 | 0.998 | 0.997 | 0.997 | 0.995 |
| **0.75** | 0.997 | 0.998 | 1.000 | 0.999 | 0.998 | 0.996 |
| **0.85** | 0.994 | 0.997 | 0.999 | 1.000 | 1.000 | 0.999 |
| **0.90** | 0.993 | 0.997 | 0.998 | 1.000 | 1.000 | 0.999 |
| **0.95** | 0.993 | 0.995 | 0.996 | 0.999 | 0.999 | 1.000 |

Toàn bộ ma trận xanh đậm, không có ô nào dưới 0.993. Tương quan thấp nhất là **ρ = 0.993** (cặp α=0.50 và α=0.90/0.95).

### Nhận xét — Mạng P2P: xếp hạng bền nhất trong 3 dataset

Điều đáng chú ý: **ρ giữa α=0.85 và α=0.90 là 1.000** (làm tròn) — tức là hai giá trị α gần nhau này cho kết quả xếp hạng hầu như đồng nhất. Điều này xảy ra do:

1. **Cấu trúc đồ thị P2P tương đối đều**: không có hub quá nổi trội, nên thay đổi α không làm thay đổi nhiều tương quan tương đối giữa các nút.
2. **Tỉ lệ dangling nodes cao (54.6%)**: phần lớn "mass" đã đi qua teleportation ngay cả khi α lớn, làm mờ đi sự khác biệt giữa các giá trị α.
3. **Hội tụ rất nhanh** (13–19 vòng) xác nhận mạng có cấu trúc đơn giản về mặt spectral.

---

## 5. So sánh Biến thể PageRank

| Biến thể | Tương quan Spearman với Standard |
|---|---|
| Standard | 1.0000 |
| Weighted | 0.9725 |
| Topic-Sensitive | 0.8986 |
| **Personalized** | **0.7334** |

Personalized PR có tương quan thấp nhất với Standard (0.733), phản ánh hiệu ứng mạnh của việc tập trung teleportation vào top-5 seed:

- **Seed pages chiếm 9%+ score mỗi page** (hạng 1–5 trong PPR), trong khi phần còn lại chỉ ~0.9%.
- Tỉ lệ score seed/non-seed ≈ **10:1** — hiệu ứng personalization rất mạnh, do mạng P2P ít có "bridge" liên kết các vùng với nhau.

---

## 6. Đặc điểm nổi bật so với wiki-Vote

| Tiêu chí | p2p-Gnutella04 | wiki-Vote |
|---|---|---|
| Dangling nodes | **5,941 (54.6%)** | 1,005 (14.1%) |
| Out-degree TB | **3.68** | 14.57 |
| In-degree tối đa | 72 | 457 |
| Chênh score #1/#20 | **1.6×** | 2.5× |
| Vòng lặp hội tụ | **18** | 29 |
| ρ_min (Spearman α) | 0.993 | 0.992 |
| Standard vs PPR | 0.733 | 0.973 |

**Kết luận:** Gnutella04 là mạng **phân tán và đồng đều** hơn wiki-Vote. Không có hub vượt trội, tỉ lệ dangling cực cao, xếp hạng ổn định với α. Tuy nhiên, **Personalized PageRank tạo ra sự thay đổi mạnh nhất** do mạng P2P thiếu kết nối liên vùng (ít bridge node).
