# Google PageRank Algorithm — Modular Implementation

A from-scratch implementation of Google's PageRank algorithm and three variants
(Personalized, Topic-Sensitive, Weighted), applied to both a synthetic graph
and three Stanford SNAP real-world datasets.

> No built-in PageRank library is used (no `networkx.pagerank`, no
> `scipy.sparse.linalg.eigs`). Only `numpy` and `matplotlib` are required.

---

## Project structure

```
Google_PaperRank_HCMUT/
├── pagerank.py                  # Entry point — orchestrates the 8-step pipeline
├── src/                         # Source package (one module per responsibility)
│   ├── __init__.py
│   ├── data_loader.py           # Download + parse Stanford SNAP edge lists
│   ├── graph.py                 # WebGraph class (synthetic + real construction)
│   ├── matrix.py                # Build link matrix P and Google matrix G
│   ├── algorithms.py            # Power Iteration: dense and sparse
│   ├── variants.py              # Personalized / Topic-Sensitive / Weighted PR
│   ├── analysis.py              # Spearman rank correlation, ranking-table printer
│   └── visualization.py         # 4 separate figures per dataset
│
├── data/                        # Cached SNAP datasets (auto-downloaded)
│   ├── wiki-Vote.txt
│   ├── p2p-Gnutella04.txt
│   └── ca-GrQc.txt
│
├── pagerank_results_synthetic/  # Output: 4 figures per dataset
├── pagerank_results_wiki-Vote/
├── pagerank_results_p2p-Gnutella04/
├── pagerank_results_ca-GrQc/
│
├── evaluation_wiki-Vote.md      # Result analysis per dataset
├── evaluation_p2p-Gnutella04.md
├── evaluation_ca-GrQc.md
├── evaluation_data_structure.md # SNAP file-format analysis across the 3 datasets
└── README.md                    # This file
```

---

## System requirements

- Python **3.10+** (uses `X | Y` and `list[int]` type hints)
- `numpy`, `matplotlib`

```bash
pip install numpy matplotlib
```

---

## How to run

```bash
# Synthetic 150-page graph (no internet)
python3 pagerank.py

# Real datasets from Stanford SNAP (downloaded once, then cached in data/)
python3 pagerank.py --real                              # default: wiki-Vote
python3 pagerank.py --real --dataset p2p-Gnutella04
python3 pagerank.py --real --dataset ca-GrQc
```

Each run prints the 8-step pipeline on the terminal and writes 4 PNG figures
into `pagerank_results_<dataset>/`:

| File | Content |
|---|---|
| `01_score_distribution.png` | PageRank score vs. rank (log scale) — power-law shape |
| `02_top20_pages.png`        | Top 20 pages bar chart, colored by topic (synthetic) |
| `03_alpha_effect.png`       | How α ∈ {0.50, 0.65, 0.75, 0.85, 0.90, 0.95} affects the Top-5 |
| `04_spearman_correlation.png` | 6×6 Spearman ρ between α values (ranking robustness) |

---

## 8-step pipeline (printed at runtime)

```
[1] Build the web graph G(V, E)
[2] Build link matrix P (column-stochastic Markov matrix)
[3] Build Google matrix G = αP + (1-α)(1/n)ee^T
[4] Compute PageRank via Power Iteration   → Top-20 table
[5] Analyze the effect of α                → 6 values, Spearman ρ, Top-10 overlap
[6] PageRank variants                      → Personalized, Topic-Sensitive, Weighted
[7] Compare Top-10 across variants         → correlation matrix
[8] Save 4 figures per dataset
```

---

## Module responsibilities

| Module | Lines | Responsibility |
|---|---|---|
| [`src/data_loader.py`](src/data_loader.py) | ~110 | SNAP URL config, downloader (gzip + cache), edge-list parser |
| [`src/graph.py`](src/graph.py) | ~140 | `WebGraph` class — synthetic builder + `from_edges()` for SNAP |
| [`src/matrix.py`](src/matrix.py) | ~60 | `build_link_matrix`, `build_google_matrix` (column-stochastic checks) |
| [`src/algorithms.py`](src/algorithms.py) | ~95 | `pagerank_power_iteration` (dense), `pagerank_sparse` (O(\|E\|)) |
| [`src/variants.py`](src/variants.py) | ~110 | Personalized / Topic-Sensitive / Weighted PageRank |
| [`src/analysis.py`](src/analysis.py) | ~55 | `spearman_rank_corr` (custom, no scipy), `print_table` |
| [`src/visualization.py`](src/visualization.py) | ~125 | `plot_results` — writes 4 separate PNGs per run |
| [`pagerank.py`](pagerank.py) | ~230 | Thin CLI entry point, runs the 8-step pipeline |

---

## ⭐ Key functions for the report

Below are the functions you should highlight in the written report.
Each one maps directly to a requirement in the project brief.

### 🔑 1. `build_link_matrix()` → Probability matrix P  *(Requirement 2)*
**File:** [`src/matrix.py`](src/matrix.py)
**Why it matters:** Defines the **column-stochastic Markov matrix** that
encodes the random-surfer transition probabilities. Critical for the report's
"probability matrix" theory section.

```python
P[j, i] = 1 / out_degree(i)   if link i → j exists
          1 / n                if i is a dangling node (no out-links)
```

Handles dangling nodes by uniform redistribution — prevents rank sinks.

---

### 🔑 2. `build_google_matrix()` → Google matrix G  *(Requirement 2)*
**File:** [`src/matrix.py`](src/matrix.py)
**Why it matters:** Combines the link matrix with teleportation to make G
**primitive** (irreducible + aperiodic). This is what enables the
Perron–Frobenius guarantee.

```python
G = α · P + (1 - α) · v · e^T,    0 < α < 1
```

- α = link-following probability
- (1-α) = teleportation probability
- v = personalization vector (uniform 1/n by default)

---

### 🔑 3. `pagerank_sparse()` → Solve π = G·π  *(Requirements 3 & 4)*
**File:** [`src/algorithms.py`](src/algorithms.py)
**Why it matters:** The main solver. **Power Iteration** in O(|E|) per
iteration — does NOT store the full n×n G matrix, so it scales to graphs
with thousands of nodes (wiki-Vote 7,115; Gnutella 10,879; ca-GrQc 5,241).

Update rule with explicit dangling-mass handling:

```python
π(k+1) = α · [ P·π(k) + d(k)·v ] + (1 - α) · v
where d(k) = Σ_{i dangling} π(k)[i]
```

Convergence guaranteed because |α·λ₂| < 1.

---

### 🔑 4. `pagerank_power_iteration()` → Dense verification  *(Requirement 3)*
**File:** [`src/algorithms.py`](src/algorithms.py)
**Why it matters:** Solves π = G·π directly on the full G matrix. Used as
a **correctness check** against `pagerank_sparse` on small graphs
(n ≤ 1000). Demonstrates the eigenvector interpretation cleanly:
π is the left eigenvector of G with eigenvalue 1.

---

### 🔑 5. `personalized_pagerank()`  *(Requirement 6a)*
**File:** [`src/variants.py`](src/variants.py)
**Why it matters:** Implements **PPR** (Page & Brin 1999) — teleportation
restricted to a seed set instead of being uniform. Result: rank concentrates
in the "neighborhood" of the seeds. Most divergent from Standard PR on
ca-GrQc (ρ = 0.169) because community structure is strong.

---

### 🔑 6. `topic_sensitive_pagerank()`  *(Requirement 6b)*
**File:** [`src/variants.py`](src/variants.py)
**Why it matters:** Implements **Haveliwala 2002** — precompute one π per
topic, return the relevant one at query time. Demonstrated on synthetic
data using the 5 built-in topics (Technology, Science, Sports, News,
Entertainment).

---

### 🔑 7. `weighted_pagerank()`  *(Requirement 6c)*
**File:** [`src/variants.py`](src/variants.py)
**Why it matters:** Implements **Xing & Ghorbani 2004** — link weight
proportional to the in-degree of the target page:

```
W(i → j) = in_deg(j) / Σ_{k: i→k} in_deg(k)
```

Pages already referenced often absorb more rank — amplifies hub effect.

---

### 🔑 8. `spearman_rank_corr()` → α-stability metric  *(Requirement 5)*
**File:** [`src/analysis.py`](src/analysis.py)
**Why it matters:** Hand-implemented (no scipy) Spearman ρ used to quantify
how much ranking changes between two α values. Drives the conclusion that
**rankings are largely invariant to α**: ρ > 0.99 on wiki-Vote / Gnutella,
ρ > 0.94 on ca-GrQc.

```
ρ = 1 - 6·Σd² / (n·(n²-1))
```

---

### 🔑 9. `WebGraph` class  *(Requirement 1)*
**File:** [`src/graph.py`](src/graph.py)
**Why it matters:** Models the directed graph G(V, E). Two construction modes:
- `WebGraph(n_pages, seed)` → 150-page synthetic graph with 5 topics and 5 hubs
- `WebGraph.from_edges(edges)` → load any SNAP edge list, remap IDs to [0, n-1]

This is the foundation everything else operates on.

---

## Theory summary

**Link matrix P** — column-stochastic Markov matrix:
```
P[j, i] = 1 / out_degree(i)   if i → j
          0                    otherwise
```

**Google matrix G** — guarantees a unique stationary distribution:
```
G = α · P + (1-α) · (1/n) · e·e^T,    0 < α < 1
```

**PageRank equation** — eigenvector problem:
```
π = G·π        →  solve via Power Iteration:  π(k+1) = G · π(k)
```

Convergence is guaranteed by the **Perron–Frobenius theorem**: G is a
primitive stochastic matrix, so its dominant eigenvalue 1 is unique and
the corresponding eigenvector π is the PageRank vector.

---

## Datasets at a glance

| Dataset | Nodes | Edges | Dangling | Type | Convergence (α=0.85) |
|---|---|---|---|---|---|
| Synthetic   | 150    | ~1,340  | 0       | Directed, 5 topics | ~30 iters |
| wiki-Vote   | 7,115  | 103,689 | 14.1%   | Directed (voting)  | 29 iters  |
| p2p-Gnutella04 | 10,876 | 39,994  | **54.6%** | Directed (P2P)     | 18 iters  |
| ca-GrQc     | 5,241  | 28,968  | 0%      | Undirected → directed (collaboration) | **118 iters** |

Detailed per-dataset analysis in `evaluation_*.md`.

---

## Sample synthetic output

```
Rank  Page        Score         Percentile  Topic
────────────────────────────────────────────────────
1     Page_060    0.02430876         99.3%  Sports
2     Page_000    0.02402535         98.7%  Technology
3     Page_120    0.02322279         98.0%  Entertainment
4     Page_030    0.02118246         97.3%  Science
5     Page_090    0.01697217         96.7%  News
```

The top-5 are exactly the 5 designed hub pages (one per topic) —
confirming the algorithm's correctness on a controlled graph.

---

## Configurable parameters

Open [`pagerank.py`](pagerank.py) and edit inside `main()`:

| Parameter | Default | Meaning |
|---|---|---|
| `n_pages` | 150 | Number of pages in the synthetic graph |
| `seed`    | 42  | RNG seed for reproducibility |
| `alpha`   | 0.85 | Damping factor (Google's original) |
| `alphas`  | `[0.50, 0.65, 0.75, 0.85, 0.90, 0.95]` | α sweep for analysis |
| `top_k`   | 20 | Rows shown in the ranking table |

---

## Notes

- The project follows the rule: **no built-in PageRank library**.
- Spearman correlation is also hand-implemented (no `scipy.stats.spearmanr`).
- For graphs with n > 1000, the full `P` and `G` matrices are skipped to
  save memory; only the sparse iterator is used.
