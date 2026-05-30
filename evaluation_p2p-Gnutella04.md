# PageRank Result Evaluation — p2p-Gnutella04 Dataset

**Dataset:** Gnutella Peer-to-Peer File Sharing Network (Stanford SNAP)
**Scale:** 10,876 nodes · 39,994 directed edges · **5,941 dangling nodes (54.6%)**
**Algorithm:** Sparse Power Iteration, α = 0.85, converged after **18 iterations** (0.088s)

---

## 1. PageRank Score Distribution (Top-left figure)

### Observation

The log-scale curve falls very steeply over the first 500 ranks, then forms a long flat tail that extends past rank 10,000. Specifically:

- **Top 1 (P01056):** score ≈ 0.00067
- **Top 20:** score ≈ 0.00042 — only about **1.6× lower** than top 1
- **Tail (rank 2,000 onward):** the curve is essentially flat around 10⁻⁴

### Comment — A very long-tail distribution

Compared with wiki-Vote, the p2p-Gnutella04 curve **is less steep at the head** but **has a much longer tail** (10,876 nodes). This reflects the nature of a P2P network:

- **No clear super-hub** — no single node dominates as in Wikipedia.
- **Flatter distribution:** the Gnutella network is designed to be evenly distributed, not centered on any single server.
- **54.6% dangling nodes** — more than half the peers have no outgoing links (peers that only receive, never forward). Teleportation plays a larger role in keeping G irreducible.

---

## 2. Top 20 Nodes (Top-right figure)

### Observation

| Rank | Node | Score |
|------|-----|-------|
| 1 | P01056 | 0.00067072 |
| 2 | P01054 | 0.00066316 |
| 3 | P01536 | 0.00054976 |
| 4 | P00171 | 0.00054385 |
| 5 | P00453 | 0.00052389 |
| … | … | … |
| 20 | P00987 | 0.00041863 |

Notable feature: **P01056 and P01054 are nearly equal** (gap < 1.2%). From rank 3 onward, scores decrease smoothly and gradually down to rank 20.

### Comment — Flat structure, no dominant hub

- **The gap between rank 1 and rank 20 is only ~1.6×** — the smallest among the three datasets. For wiki-Vote, the ratio is 2.5×.
- This reflects the **decentralized structure of a P2P network**: peers (nodes) are designed to be equivalent, with no single peer acting as an absolute "server".
- **The maximum in-degree is only 72** — far below wiki-Vote (457). This is a hallmark of first-generation P2P networks (Gnutella): per-peer connection limits to avoid congestion.

---

## 3. Effect of Damping Factor α (Bottom-left figure)

### Observation

Five colored lines correspond to the top-5 nodes as α grows from 0.5 to 0.95:

- **All five lines are nearly parallel with similar slopes** — none surges or collapses sharply.
- The gaps between the five lines **change little** as α increases.
- At α = 0.50: scores ≈ 0.00042–0.00043 (very close together).
- At α = 0.95: scores ≈ 0.00063–0.00075 (still close, similar ratio).
- **No lines cross** — the ranking order is completely stable.

### Comment — Extremely stable rankings

| α | Top node | Score | Iter | ρ (Spearman) |
|---|-----------|-------|------|------|
| 0.50 | P01054 | 0.00043 | 13 | 0.9938 |
| 0.65 | P01054 | 0.00053 | 15 | 0.9978 |
| 0.75 | P01054 | 0.00060 | 16 | 0.9994 |
| 0.85 | P01056 | 0.00067 | 18 | 1.0000 |
| 0.90 | P01056 | 0.00071 | 18 | 0.9999 |
| 0.95 | P01056 | 0.00075 | 19 | 0.9994 |

Note: **P01054 and P01056 swap the #1 position when α crosses ~0.80** — a visual demonstration that α can affect rankings where scores are very close, even though overall correlation remains high (ρ > 0.993).

---

## 4. Spearman Correlation Matrix (Bottom-right figure)

### Observation

| | 0.50 | 0.65 | 0.75 | 0.85 | 0.90 | 0.95 |
|--|--|--|--|--|--|--|
| **0.50** | 1.000 | 0.994 | 0.997 | 0.994 | 0.993 | 0.993 |
| **0.65** | 0.994 | 1.000 | 0.998 | 0.997 | 0.997 | 0.995 |
| **0.75** | 0.997 | 0.998 | 1.000 | 0.999 | 0.998 | 0.996 |
| **0.85** | 0.994 | 0.997 | 0.999 | 1.000 | 1.000 | 0.999 |
| **0.90** | 0.993 | 0.997 | 0.998 | 1.000 | 1.000 | 0.999 |
| **0.95** | 0.993 | 0.995 | 0.996 | 0.999 | 0.999 | 1.000 |

The entire matrix is dark green, with no cell below 0.993. The minimum is **ρ = 0.993** (pairs α=0.50 with α=0.90/0.95).

### Comment — P2P network: most ranking-stable of the three

Worth highlighting: **ρ between α=0.85 and α=0.90 is 1.000** (rounded) — these two nearby α values yield essentially identical rankings. This happens because:

1. **Even P2P graph structure**: no node is excessively prominent, so changing α does not significantly alter the relative correlation between nodes.
2. **High dangling fraction (54.6%)**: a large share of mass already flows through teleportation even at large α, blurring the differences between α values.
3. **Very fast convergence** (13–19 iterations) confirms a spectrally simple structure.

---

## 5. PageRank Variant Comparison

| Variant | Spearman correlation with Standard |
|---|---|
| Standard | 1.0000 |
| Weighted | 0.9725 |
| Topic-Sensitive | 0.8986 |
| **Personalized** | **0.7334** |

Personalized PR has the lowest correlation with Standard (0.733), reflecting the strong effect of concentrating teleportation on top-5 seeds:

- **Seed pages take 9%+ of score each** (ranks 1–5 in PPR), while the rest get only ~0.9%.
- The seed/non-seed score ratio is ~**10:1** — a very strong personalization effect, because the P2P network has few "bridge" links connecting different regions.

---

## 6. Distinctive Features vs. wiki-Vote

| Criterion | p2p-Gnutella04 | wiki-Vote |
|---|---|---|
| Dangling nodes | **5,941 (54.6%)** | 1,005 (14.1%) |
| Average out-degree | **3.68** | 14.57 |
| Max in-degree | 72 | 457 |
| Score ratio #1/#20 | **1.6×** | 2.5× |
| Convergence iterations | **18** | 29 |
| ρ_min (Spearman over α) | 0.993 | 0.992 |
| Standard vs PPR | 0.733 | 0.973 |

**Conclusion:** Gnutella04 is a **more distributed and uniform** network than wiki-Vote. It has no dominant hub, an extremely high dangling fraction, and rankings stable under α. However, **Personalized PageRank produces the largest deviation** because the P2P network lacks cross-region connectivity (few bridge nodes).
