# Đánh giá Cấu trúc Dữ liệu — Ba Dataset SNAP

Tài liệu này phân tích định dạng file, ý nghĩa từng cột, và đặc trưng thống kê của ba dataset được tải về từ Stanford SNAP để chạy PageRank.

---

## 1. Định dạng chung — SNAP Edge List

Cả ba file đều theo **định dạng SNAP edge list**:

```
# Dòng comment bắt đầu bằng #
# Nodes: <n>  Edges: <m>
# FromNodeId    ToNodeId
<src>   <dst>
<src>   <dst>
...
```

**Quy tắc đọc:**
- Dòng bắt đầu bằng `#` → bỏ qua (metadata/comment).
- Mỗi dòng dữ liệu gồm **hai số nguyên** cách nhau bởi tab: `src` và `dst`.
- Mỗi dòng = **một cạnh có hướng** từ nút `src` đến nút `dst`.
- Node ID là số nguyên tùy ý (không nhất thiết liên tục từ 0).
- Self-loop (`src == dst`) không xuất hiện trong ba dataset này.
- **Không có trọng số cạnh** — đồ thị nhị phân (0/1).

**Cách chương trình xử lý:**
```python
# Hàm load_snap_edges() trong pagerank.py
edges = []
for line in file:
    if line.startswith('#'): continue
    src, dst = map(int, line.split())
    if src != dst:
        edges.append((src, dst))

# Hàm WebGraph.from_edges() remap về [0, n-1]
all_nodes = sorted(set(u for e in edges for u in e))
remap = {old: new for new, old in enumerate(all_nodes)}
```

---

## 2. wiki-Vote.txt

### 2.1 Header và ý nghĩa

```
# Directed graph (each unordered pair of nodes is saved once): Wiki-Vote.txt
# Wikipedia voting on promotion to administratorship (till January 2008).
# Directed edge A->B means user A voted on B becoming Wikipedia administrator.
# Nodes: 7115  Edges: 103689
# FromNodeId    ToNodeId
30      1412
30      3352
...
```

**Giải thích:**
- **Nút** = người dùng Wikipedia (được định danh bằng ID số nguyên).
- **Cạnh A → B** = người dùng A đã bỏ phiếu cho B trong cuộc bầu chọn admin.
- Dữ liệu thu thập đến tháng 1/2008, bao gồm tất cả lịch sử bỏ phiếu.
- Một người dùng có thể bỏ nhiều phiếu (nhiều dòng từ cùng một `src`).
- **Không lưu phiếu thuận/phản** — chỉ ghi nhận hành động bỏ phiếu.

### 2.2 Thống kê cấu trúc

| Chỉ số | Giá trị |
|---|---|
| Số nút | 7,115 |
| Số cạnh (unique) | 103,689 |
| Duplicate edges | 0 |
| Out-degree trung bình | 14.57 |
| Out-degree trung vị | **2.0** |
| Out-degree lệch chuẩn | 42.28 |
| Out-degree tối đa | **893** (nút 2565) |
| In-degree tối đa | **457** (nút 4037) |
| Dangling nodes (out=0) | 1,005 (14.1%) |
| Source-only nodes (in=0) | **4,734 (66.5%)** |
| Cạnh đối xứng (A→B và B→A) | 2,927 (2.8%) |

### 2.3 Phân phối out-degree

```
   =0:  1005  █████
    1:  2382  █████████████
    2:   704  ███
  3-5:   842  ████
 6-10:   570  ███
11-20:   513  ██
21-50:   577  ███
51-100:  296  █
  100+:  226  █
```

### 2.4 Nhận xét và cách hiểu

**Quan sát 1: Đa số người dùng chỉ bỏ 1–2 phiếu, nhưng một số ít bỏ hàng trăm phiếu.**

Mean = 14.57 nhưng median = 2 và stdev = 42.28 — phân phối lệch phải cực mạnh (heavy-tailed). Nút 2565 bỏ tới **893 phiếu** (tương đương tham gia ~893 cuộc bầu chọn), trong khi đại đa số chỉ bỏ 1–2.

**Quan sát 2: 66.5% nút có in-degree = 0 — không bao giờ được bầu.**

Hơn 2/3 người dùng Wikipedia chưa bao giờ ứng cử làm admin, hoặc ứng cử nhưng không có phiếu nào được ghi nhận. Đây là nhóm "voter thuần túy".

**Quan sát 3: Chỉ 2.8% cạnh đối xứng — bỏ phiếu qua lại rất hiếm.**

Hành động A → B (A bầu B) gần như không bao giờ kéo theo B → A. Đây là đặc trưng của đồ thị **bỏ phiếu bất đối xứng** — ảnh hưởng tới PageRank: người bỏ nhiều phiếu (out-degree cao) không nhất thiết nhận được nhiều phiếu (in-degree cao).

**Ý nghĩa PageRank:**
- Nút in-degree cao (nút 4037: 457 phiếu) = người được cộng đồng tín nhiệm nhất.
- Nút out-degree cao (nút 2565: 893 phiếu) = người hoạt động bầu chọn nhiều nhất nhưng PageRank thấp vì không được ai bầu lại.
- Top-5 in-degree và top-5 out-degree là **các nút hoàn toàn khác nhau** — chứng minh PageRank đo "uy tín nhận được" khác với "mức độ hoạt động".

---

## 3. p2p-Gnutella04.txt

### 3.1 Header và ý nghĩa

```
# Directed graph (each unordered pair of nodes is saved once): p2p-Gnutella04.txt
# Directed Gnutella P2P network from August 4 2002
# Nodes: 10876  Edges: 39994
# FromNodeId    ToNodeId
0       1
0       2
0       3
...
```

**Giải thích:**
- **Nút** = một máy tính (peer) tham gia mạng Gnutella vào ngày 04/08/2002.
- **Cạnh A → B** = peer A biết địa chỉ của peer B và có thể gửi truy vấn tìm file đến B.
- Gnutella là mạng chia sẻ file P2P thế hệ đầu (không có máy chủ trung tâm).
- Node ID từ 0 liên tục — đây là snapshot một thời điểm trong ngày.

### 3.2 Thống kê cấu trúc

| Chỉ số | Giá trị |
|---|---|
| Số nút | 10,876 |
| Số cạnh (unique) | 39,994 |
| Duplicate edges | 0 |
| Out-degree trung bình | 3.68 |
| Out-degree trung vị | **0.0** |
| Out-degree lệch chuẩn | 4.92 |
| Out-degree tối đa | **100** (nút 3109) |
| In-degree tối đa | **72** (nút 1054) |
| Dangling nodes (out=0) | **5,941 (54.6%)** |
| Source-only nodes (in=0) | 20 (0.2%) |
| Cạnh đối xứng | **0 (0.0%)** |

### 3.3 Phân phối out-degree

```
   =0:  5941  █████████████████████
    1:   807  ██
    2:    73
  3-5:   242
 6-10:  3765  █████████████
11-20:    30
21-50:    14
51-100:    4
  100+:    0
```

### 3.4 Nhận xét và cách hiểu

**Quan sát 1: Phân phối out-degree lưỡng đỉnh (bimodal) — 0 hoặc 6–10.**

Đây là đặc điểm nổi bật nhất của Gnutella. Lý do kỹ thuật: giao thức Gnutella quy định mỗi peer khi tham gia phải kết nối đến một số cố định peer khác (thường là **ultrapeer**, khoảng 6–10 kết nối). Peer không đủ năng lực sẽ hoạt động ở chế độ **leaf** (lá) — chỉ nhận, không chuyển tiếp — dẫn đến out-degree = 0.

**Quan sát 2: 0% cạnh đối xứng — kết nối một chiều hoàn toàn.**

Không có bất kỳ cặp (A→B, B→A) nào. Trong Gnutella, kết nối không tự động hai chiều: A biết B không có nghĩa B biết A. Điều này tạo ra đồ thị **có hướng bất đối xứng tuyệt đối**.

**Quan sát 3: 54.6% nút là "leaf" (lá) — chỉ nhận, không chuyển tiếp.**

Hơn nửa số peer không có liên kết ra (out-degree = 0). Đây là dangling nodes — trong PageRank, rank của chúng được phân phối đồng đều qua cơ chế teleportation thay vì chảy qua liên kết. Điều này giải thích tại sao p2p-Gnutella04 hội tụ **nhanh nhất** (18 vòng): phần lớn mass đã được "làm phẳng" ngay từ đầu.

**Ý nghĩa PageRank:**
- Peer có in-degree cao (nút 1054: 72) = **ultrapeer nổi tiếng**, được nhiều peer khác trỏ đến để tìm file.
- Các nút 0, 1, 2... được kết nối tuần tự trong snapshot → phản ánh thứ tự tham gia mạng theo thời gian thực.
- Không thể có "bỏ phiếu lại" (0% reciprocal) → cấu trúc phân cấp rõ ràng (ultrapeer → leaf).

---

## 4. ca-GrQc.txt

### 4.1 Header và ý nghĩa

```
# Directed graph (each unordered pair of nodes is saved once): CA-GrQc.txt
# Collaboration network of Arxiv General Relativity category
# (there is an edge if authors coauthored at least one paper)
# Nodes: 5242  Edges: 28980
# FromNodeId    ToNodeId
3466    937
3466    5233
3466    8579
...
10310   3466      ← cạnh ngược: 10310 cũng đồng tác giả với 3466
```

**Giải thích:**
- **Nút** = nhà khoa học có ít nhất một bài báo trên arXiv danh mục General Relativity & Quantum Cosmology.
- **Cạnh A → B** = A và B đã **đồng tác giả** ít nhất một bài báo.
- Đây là **đồ thị vô hướng** (undirected) nhưng SNAP lưu dưới dạng directed bằng cách ghi cả hai chiều:  
  `A → B` và `B → A` đều xuất hiện trong file.
- Node ID là số nguyên tùy ý (không liên tục, range rộng như 3466, 8579, 19607...).

### 4.2 Thống kê cấu trúc

| Chỉ số | Giá trị |
|---|---|
| Số nút | 5,241 |
| Số cạnh (unique) | 28,968 |
| Duplicate edges | 0 |
| Out-degree trung bình | 5.53 |
| Out-degree trung vị | **3.0** |
| Out-degree lệch chuẩn | 7.92 |
| Out-degree tối đa | **81** (nút 21012) |
| In-degree tối đa | **81** (nút 21012) — **cùng nút!** |
| Dangling nodes (out=0) | **0 (0.0%)** |
| Source-only nodes (in=0) | **0 (0.0%)** |
| Cạnh đối xứng | **14,484 (50.0%)** |

Top-5 in-degree = Top-5 out-degree = **cùng 5 nút, cùng giá trị** → xác nhận đây là đồ thị symmetric.

### 4.3 Phân phối out-degree

```
   =0:     0
    1:  1197  █████████
    2:  1115  ████████
  3-5:  1568  ███████████
 6-10:   717  █████
11-20:   389  ██
21-50:   233  █
51-100:   22
  100+:    0
```

### 4.4 Nhận xét và cách hiểu

**Quan sát 1: Đúng 50.0% cạnh đối xứng — đồ thị vô hướng lưu dưới dạng directed.**

Header SNAP ghi "each unordered pair of nodes is saved once" nhưng thực tế **mỗi cạnh vô hướng được lưu thành 2 cạnh có hướng**. Ví dụ cạnh (3466, 10310) xuất hiện ở cả hai dạng:
- Dòng `3466 → 10310` (từ bộ cạnh của nút 3466)
- Dòng `10310 → 3466` (từ bộ cạnh của nút 10310)

Đây là lý do in-degree = out-degree tuyệt đối cho mọi nút.

**Quan sát 2: Không có dangling node, không có source-only node.**

Mọi nhà khoa học trong dataset đều có ít nhất 1 cộng tác viên theo cả hai chiều. Dataset chỉ bao gồm component liên thông lớn nhất (giant component), loại bỏ các tác giả cô lập.

**Quan sát 3: Node ID rất thưa và không liên tục (3466, 8579, 19607...).**

Đây là ID nội bộ của arXiv, không liên tục trong [0, 5241]. Hàm `WebGraph.from_edges()` phải remap về [0, 4] để dùng làm index mảng. Điều này giải thích tại sao output hiển thị `P00000..P05240` thay vì ID gốc.

**Quan sát 4: Phân phối out-degree gần Normal lệch phải (median=3, max=81).**

Không có nút "siêu hub" như wiki-Vote (893) hay Gnutella (100). Nhà khoa học đa cộng tác nhất (nút 21012) có 81 đồng tác giả — phản ánh nhóm nghiên cứu lớn trong vật lý lý thuyết.

**Ý nghĩa PageRank:**
- Trong đồ thị symmetric: **PageRank ≈ Degree Centrality** — nút có nhiều cộng tác nhất thường đứng đầu.
- Nhưng không hoàn toàn: PageRank là **weighted degree** qua eigenvector — nút kết nối với hub quan trọng hơn nút kết nối với leaf (như P02773 đánh bại P04281 dù cùng degree cao).
- Eigenvalue thứ hai (λ₂) gần 1 trong mạng symmetric → **hội tụ chậm** (118 vòng so với 18–29 vòng của hai dataset kia).

---

## 5. So sánh Cấu trúc Ba Dataset

### 5.1 Bảng tổng hợp

| Đặc điểm | wiki-Vote | p2p-Gnutella04 | ca-GrQc |
|---|---|---|---|
| **Loại mạng** | Bỏ phiếu (directed) | P2P file sharing (directed) | Cộng tác KH (undirected → directed) |
| **Nút / Cạnh** | 7,115 / 103,689 | 10,876 / 39,994 | 5,241 / 28,968 |
| **Node ID** | Không liên tục | Liên tục từ 0 | Rất thưa (arXiv ID) |
| **Density** = 2\|E\|/\|V\|(\|V\|-1) | 0.41% | 0.034% | 0.21% |
| **Out-degree median** | 2 | **0** | 3 |
| **Out-degree stdev** | **42.28** | 4.92 | 7.92 |
| **Dangling nodes** | 14.1% | **54.6%** | **0%** |
| **Source-only (in=0)** | **66.5%** | 0.2% | 0% |
| **Cạnh đối xứng** | 2.8% | **0%** | **50%** |
| **Vòng hội tụ PR** | 29 | **18** | **118** |

### 5.2 Đặc trưng riêng từng loại đồ thị

```
wiki-Vote:
  Rất bất đối xứng nhưng theo chiều "out":
  ┌─────────────────────────────────────┐
  │  Người bỏ phiếu nhiều ──→ hub admin│
  │  (out=893)          (in=457)        │
  │  66.5% nút không nhận phiếu nào    │
  └─────────────────────────────────────┘
  → PageRank đo uy tín nhận được, không phải mức độ tham gia

p2p-Gnutella04:
  Cấu trúc phân tầng rõ ràng (phân phối bimodal):
  ┌─────────────────────────────────────┐
  │  Leaf peers (out=0) ────→ Ultrapeer│
  │  54.6%                  (in=72)    │
  │  0% cạnh đối xứng                 │
  └─────────────────────────────────────┘
  → PageRank đo khả năng "tiếp cận" trong mạng P2P

ca-GrQc:
  Đồ thị vô hướng lưu dạng directed, symmetric hoàn toàn:
  ┌─────────────────────────────────────┐
  │  A ←→ B (mỗi cộng tác = 2 cạnh)   │
  │  in-degree ≡ out-degree             │
  │  0 dangling, 50% reciprocal         │
  └─────────────────────────────────────┘
  → PageRank ≈ Eigenvector Centrality của đồ thị vô hướng
```

### 5.3 Tác động đến thuật toán PageRank

| Đặc trưng dữ liệu | Tác động đến PageRank |
|---|---|
| **Dangling nodes cao (Gnutella 54.6%)** | Cần cơ chế teleportation mạnh; hội tụ nhanh do mass được "làm phẳng" |
| **Source-only cao (wiki-Vote 66.5%)** | Phần lớn nút không nhận rank từ liên kết; rank chủ yếu từ (1-α)·v |
| **0% reciprocal (Gnutella)** | Cấu trúc cây/DAG → dễ hội tụ, ít vòng lặp |
| **50% reciprocal (ca-GrQc)** | Mạng symmetric → λ₂ ≈ 1 → hội tụ rất chậm (118–374 vòng) |
| **Out-degree stdev cao (wiki-Vote 42.28)** | Phân phối power-law mạnh → top hub vượt trội rõ ràng |
| **Node ID không liên tục (ca-GrQc)** | Cần bước remap về [0,n-1] trước khi dùng làm chỉ số mảng |
