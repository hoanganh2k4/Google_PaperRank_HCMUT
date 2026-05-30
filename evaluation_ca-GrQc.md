# PageRank Result Evaluation — ca-GrQc Dataset

**Dataset:** Collaboration Network — arXiv General Relativity & Quantum Cosmology (Stanford SNAP)
**Scale:** 5,241 nodes · 28,968 edges · **0 dangling nodes** · max in-degree = max out-degree = 81
**Algorithm:** Sparse Power Iteration, α = 0.85, converged after **118 iterations** (0.414s)

> **Important characteristic:** ca-GrQc is a scientific collaboration network (an undirected graph represented as directed by adding both directions for each edge). This produces **in-degree = out-degree** for every node — a fundamental difference from the other two datasets.

---

## 1. PageRank Score Distribution (Top-left figure)

### Observation

The log-scale curve has a **noticeably different shape** from Gnutella04 and wiki-Vote:

- **Not steep at the head** — it decreases relatively evenly from rank 1 to about rank 3,000.
- **Middle region (ranks 1,000–3,500):** roughly constant slope, close to linear on log scale.
- **Tail (rank 4,000+):** an abrupt "cliff" — many nodes share extremely small scores near zero.
- **Top-1 score (≈ 0.00144) is lower than wiki-Vote (0.00461)** despite fewer nodes — indicating that rank is more evenly distributed.

### Comment — Collaboration networks have a smoother distribution

Due to the **symmetric** nature of the collaboration network:

- Rank "flows" in both directions across each edge → no node accumulates rank from one side without contributing back.
- No web-style super-hub forms (a page that attracts inbound links without sending any out).
- **Research communities** (cliques) produce clusters of nodes with similar scores within each cluster, yielding a smoother curve.
- The cliff at the tail corresponds to isolated scientists (only 1–2 collaborations), pruned from the giant connected component.

---

## 2. Top 20 Nodes (Top-right figure)

### Observation

| Rank | Node | Score |
|------|-----|-------|
| 1 | P02773 | 0.00144317 |
| 2 | P02713 | 0.00134123 |
| 3 | P02725 | 0.00130603 |
| 4 | P04281 | 0.00117802 |
| 5 | P01934 | 0.00116955 |
| … | … | … |
| 20 | P01489 | 0.00091651 |

The ratio top-1 / top-20 is **1.57×** — comparable to Gnutella04, indicating a fairly uniform distribution among leading nodes.

### Comment — Top nodes are "bridge" scientists

In a collaboration network, a node with high PageRank is not only "famous" (with many connections) but also someone who **bridges multiple research groups**:

- P02773 (rank 1) likely has in-degree = out-degree = 81 and sits at the center of multiple clusters.
- In a symmetric network: **PageRank ≈ Degree Centrality** — the node with the most collaborators typically ranks at the top.
- But not strictly: P04281 (rank 4) has in-degree = 81 like P02773, yet ranks lower — because P02773 connects to higher-ranked nodes (eigenvector centrality effect).

---

## 3. Effect of Damping Factor α (Bottom-left figure)

### Observation — A special phenomenon: lines crossing

Five colored lines show **clear instability** as α grows large:

- **P04281 (orange/yellow):** starts low (α=0.5) but rises sharply, **crossing the other lines** around α ≈ 0.85–0.90 and reaching **the highest score at α = 0.95**.
- **P02773 (red):** leads at low and medium α, but is overtaken by P04281 at high α.
- **P02725 (green) and P02713 (blue):** rise steadily but cannot maintain their margin.
- Result: **the top node changes from P02773 to P04232 at α = 0.95**.

| α | Top node | Score | Iterations | ρ (Spearman) |
|---|---|---|---|---|
| 0.50 | P02773 | 0.001131 | 28 | 0.9758 |
| 0.65 | P02773 | 0.001307 | 45 | 0.9872 |
| 0.75 | P02773 | 0.001394 | 67 | 0.9942 |
| 0.85 | P02773 | 0.001443 | **118** | 1.0000 |
| 0.90 | P02773 | 0.001442 | **182** | 0.9962 |
| 0.95 | **P04232** | 0.001586 | **374** | 0.9877 |

**Key observations:**

1. **Iteration count explodes as α grows** (28 → 374): in a symmetric network the second eigenvalue of P (λ₂) is closer to 1, making the |α·λ₂| convergence rate much slower for large α.

2. **P02773's score peaks at α=0.85** then slightly decreases at α=0.90 — an unusual phenomenon: for a symmetric network, λ₂ ≈ 1 pulls the rank distribution toward the second eigenvector as α → 1, leading to **rank oscillations at very high α**.

3. **Top-10 overlap at α=0.95 drops to 6/10** — the lowest among the three datasets, demonstrating higher α-sensitivity in collaboration networks.

---

## 4. Spearman Correlation Matrix (Bottom-right figure)

### Observation

The matrix is **non-uniform** in color — yellow/light-green cells appear in the α=0.95 column/row and the α=0.50 row:

| | 0.50 | 0.65 | 0.75 | 0.85 | 0.90 | 0.95 |
|--|--|--|--|--|--|--|
| **0.50** | 1.000 | 0.985 | 0.975 | 0.976 | 0.965 | **0.946** |
| **0.65** | 0.985 | 1.000 | 0.995 | 0.987 | 0.979 | 0.963 |
| **0.75** | 0.975 | 0.995 | 1.000 | 0.994 | 0.988 | 0.975 |
| **0.85** | 0.976 | 0.987 | 0.994 | 1.000 | 0.996 | 0.984 |
| **0.90** | 0.965 | 0.979 | 0.988 | 0.996 | 1.000 | **0.994** |
| **0.95** | **0.946** | 0.963 | 0.975 | 0.984 | 0.994 | 1.000 |

**Minimum correlation: ρ = 0.946** (pair α=0.50 and α=0.95) — substantially lower than wiki-Vote (0.992) and Gnutella04 (0.993).

### Comment — Why is ca-GrQc more sensitive to α?

The root cause lies in the **spectral structure** of the graph:

- **Symmetric collaboration network → real eigenvalues of P close to 1**: in an undirected graph, multiple eigenvalues can approach 1, making |α·λ₂| ≈ α → slow convergence and α-sensitivity.
- **Strong community structure (internal cliques):** each research group is a near-complete clique. As α changes, weight between communities shifts, potentially raising different nodes to the top.
- **Zero dangling nodes:** no natural smoothing via dangling teleportation as in Gnutella04.

---

## 5. PageRank Variant Comparison

| Variant | Spearman correlation with Standard |
|---|---|
| Standard | 1.0000 |
| Weighted | 0.9541 |
| Topic-Sensitive | 0.5369 |
| **Personalized** | **0.1691** |

**Personalized PR correlates only 0.169 with Standard** — extremely divergent, the lowest among all three datasets. Reasons:

- **Isolated community structure**: the seeds (top-5 in-degree nodes) belong to a few scientific clusters. When teleportation only routes to seeds, rank concentrates within their cluster and is fully isolated from the rest of the network.
- **"Community bubble" effect**: PPR results are entirely different from Standard because, in a collaboration network, a scientist outside the seed's community is effectively invisible to PPR.

---

## 6. Comparison Across the Three Real Datasets

| Criterion | wiki-Vote | p2p-Gnutella04 | **ca-GrQc** |
|---|---|---|---|
| Graph type | Directed (voting) | Directed (P2P) | Undirected → directed |
| Nodes / Edges | 7,115 / 103,689 | 10,876 / 39,994 | 5,241 / 28,968 |
| Dangling nodes | 14.1% | 54.6% | **0%** |
| Max in-degree | 457 | 72 | **81 = Max out-degree** |
| Iterations (α=0.85) | 29 | 18 | **118** |
| ρ_min Spearman (α) | 0.992 | 0.993 | **0.946** |
| Standard vs PPR | 0.973 | 0.733 | **0.169** |
| Top-10 overlap (α=0.95) | 10/10 | 9/10 | **6/10** |

**Conclusion:** ca-GrQc is the **hardest dataset to converge on** and **most α-sensitive** of the three. The cause is the symmetric nature of the collaboration network producing a second eigenvalue close to 1. This is a textbook example showing that **PageRank was originally designed for asymmetric directed web graphs** — when applied to a symmetric collaboration network, parameters such as α must be calibrated more carefully.
