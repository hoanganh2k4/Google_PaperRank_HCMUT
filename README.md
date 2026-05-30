# Google PageRank Algorithm — Hướng dẫn Cài đặt & Chạy

## Yêu cầu hệ thống

- Python **3.10+** (dùng type hint `X | Y` và `list[int]`)
- pip

---

## Cài đặt

### 1. Kiểm tra phiên bản Python

```bash
python3 --version
```

Kết quả phải là `Python 3.10.x` trở lên.

### 2. Cài đặt thư viện

Chương trình chỉ dùng **2 thư viện chuẩn**:

| Thư viện | Mục đích |
|---|---|
| `numpy` | Đại số tuyến tính, nhân ma trận |
| `matplotlib` | Vẽ biểu đồ |

```bash
pip install numpy matplotlib
```

Hoặc nếu dùng môi trường ảo:

```bash
python3 -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate       # Windows

pip install numpy matplotlib
```

> **Lưu ý:** Chương trình **không** dùng bất kỳ thư viện PageRank có sẵn nào (networkx, scipy.sparse.linalg.eigs, v.v.).

---

## Chạy chương trình

### Chế độ 1 — Đồ thị tự sinh (150 trang, không cần internet)

```bash
cd /home/haa900/DSTT
python3 pagerank.py
```

### Chế độ 2 — Dataset thực từ Stanford SNAP (cần internet lần đầu)

```bash
# Wikipedia voting network (7,115 nút, 103,689 cạnh) — mặc định
python3 pagerank.py --real

# Gnutella P2P network (10,879 nút, 39,994 cạnh)
python3 pagerank.py --real --dataset p2p-Gnutella04

# Collaboration network arxiv GR-QC (5,242 nút, 28,980 cạnh)
python3 pagerank.py --real --dataset ca-GrQc
```

> Dataset được tải về và cache tại `DSTT/data/` — lần sau chạy không cần tải lại.

---

## Output khi chạy

### Terminal

Chương trình in tuần tự 8 bước:

```
[1] Xây dựng đồ thị web G(V, E) với 150 trang
[2] Xây dựng ma trận liên kết P (150×150)
[3] Xây dựng Google Matrix G với α = 0.85
[4] Tính PageRank bằng Power Iteration
    → Bảng xếp hạng Top 20
[5] Phân tích ảnh hưởng của α ∈ {0.50, 0.65, 0.75, 0.85, 0.90, 0.95}
[6] Các biến thể PageRank
    [6a] Personalized PageRank
    [6b] Topic-Sensitive PageRank
    [6c] Weighted PageRank
[7] So sánh Top-10 giữa các biến thể
[8] Lưu biểu đồ trực quan
```

### File ảnh

Biểu đồ được lưu tự động theo chế độ:

```
DSTT/pagerank_results_synthetic.png   ← chế độ tự sinh
DSTT/pagerank_results_wiki-Vote.png   ← chế độ --real --dataset wiki-Vote
DSTT/pagerank_results_p2p-Gnutella04.png
DSTT/data/wiki-Vote.txt               ← cache dataset (tải 1 lần)
```

Gồm 4 panel:
- **Phân phối score** (log scale) — dạng power law
- **Top 20 trang** (màu theo chủ đề)
- **Ảnh hưởng của α** lên Top-5 trang
- **Ma trận tương quan Spearman** giữa các giá trị α

---

## Cấu trúc chương trình

```
pagerank.py
├── WebGraph                   # Đồ thị web G(V, E) — 150 trang, 5 chủ đề
├── build_link_matrix()        # Ma trận P (column-stochastic)
├── build_google_matrix()      # G = αP + (1-α)(1/n)ee^T
├── pagerank_power_iteration() # Power Iteration trên ma trận đầy đủ
├── pagerank_sparse()          # Power Iteration trên đồ thị thưa (hiệu quả hơn)
├── personalized_pagerank()    # Biến thể: Personalized PageRank
├── topic_sensitive_pagerank() # Biến thể: Topic-Sensitive PageRank
├── weighted_pagerank()        # Biến thể: Weighted PageRank
├── analyze_alpha()            # Phân tích ảnh hưởng của α
├── spearman_rank_corr()       # Tương quan hạng Spearman (tự cài, không dùng scipy)
├── print_table()              # In bảng xếp hạng
├── plot_results()             # Vẽ và lưu biểu đồ
└── main()                     # Điều phối toàn bộ
```

---

## Tham số có thể chỉnh

Mở `pagerank.py` và sửa trong hàm `main()`:

| Tham số | Vị trí | Mặc định | Ý nghĩa |
|---|---|---|---|
| `n_pages` | `WebGraph(n_pages=150)` | 150 | Số trang web |
| `seed` | `WebGraph(seed=42)` | 42 | Seed sinh đồ thị ngẫu nhiên |
| `alpha` | `alpha = 0.85` | 0.85 | Damping factor (Google dùng 0.85) |
| `alphas` | `alphas = [...]` | 6 giá trị | Danh sách α để phân tích |
| `seed_pages` | `seed = list(range(5))` | [0..4] | Trang seed cho Personalized PR |
| `query_topic` | `query_topic="Science"` | Science | Chủ đề truy vấn cho Topic-Sensitive PR |
| `top_k` | `print_table(..., top_k=20)` | 20 | Số trang hiển thị trong bảng |

---

## Ví dụ kết quả

```
Rank  Trang       Score         Percentile  Chủ đề
────────────────────────────────────────────────────
1     Page_060    0.02430876         99.3%  Sports
2     Page_000    0.02402535         98.7%  Technology
3     Page_120    0.02322279         98.0%  Entertainment
4     Page_030    0.02118246         97.3%  Science
5     Page_090    0.01697217         96.7%  News
```

---

## Lý thuyết tóm tắt

**Ma trận P** — Column-stochastic Markov matrix:
```
P[j,i] = 1 / out_degree(i)   nếu i → j
         0                    ngược lại
```

**Google Matrix** — Đảm bảo hội tụ:
```
G = α·P + (1-α)·(1/n)·ee^T,    0 < α < 1
```

**Phương trình PageRank** — Eigenvector problem:
```
π = G·π   →   giải bằng Power Iteration:  π(k+1) = G·π(k)
```

Hội tụ đảm bảo bởi **Định lý Perron-Frobenius**: G là ma trận nguyên thủy nên eigenvalue trội = 1 là duy nhất.
