# PageRank Result Evaluation — wiki-Vote Dataset

**Dataset:** Wikipedia Voting Network (Stanford SNAP)
**Scale:** 7,115 nodes · 103,689 directed edges · 1,005 dangling nodes
**Algorithm:** Sparse Power Iteration, α = 0.85, converged after 29 iterations

---

## 1. PageRank Score Distribution (Top-left figure)

### Observation

On a log-scaled Y-axis, the curve drops very steeply at the head and then flattens toward the tail. Specifically:

- **Top 1 page (P03649):** score ≈ 0.0046 — about **2.5× higher** than the page at rank 20
- **Top ~50 pages:** score ≥ 10⁻³, accounting for most of the total rank mass
- **From rank 1,000 onward:** the curve flattens around 10⁻⁴ — thousands of pages share nearly identical scores

### Comment — Power-Law Distribution

The shape of the curve on a log scale matches a **power-law (long-tail) distribution**:

$$\pi(k) \sim k^{-\gamma}$$

This is the canonical signature of a real-world web graph:
- **A small set of hub pages dominates** — they receive inbound links from across the network.
- **The vast majority of pages have low rank** — few inbound links, scores close to the baseline.
- This reflects the **"rich get richer"** principle (Barabási–Albert): popular pages are more likely to attract new links.

In wiki-Vote, this corresponds to: **Wikipedia users with higher reputation receive proportionally more trust votes from others**, producing a clearly asymmetric link structure.

---

## 2. Top 20 Pages (Top-right figure)

### Observation

| Rank | Page | Score |
|------|-------|-------|
| 1 | P03649 | 0.00461 |
| 2 | P00012 | 0.00368 |
| 3 | P05806 | 0.00359 |
| 4 | P02410 | 0.00328 |
| 5 | P02204 | 0.00261 |
| … | … | … |
| 20 | P03064 | 0.00178 |

The bars decrease almost linearly from rank 1 to rank 20, showing **no sudden gap** within the top group — this is a homogeneous "authority cluster".

### Comment — Link structure determines ranking

- **P03649** leads with the highest in-degree (457 inbound links) — the Wikipedia user with the most trust votes.
- The top-5 collectively hold a much larger share of score than the rest, reflecting the **concentrated hub structure** of the voting network.
- No isolated outlier — all top-20 pages belong to a highly interconnected "high-authority" region.

---

## 3. Effect of Damping Factor α (Bottom-left figure)

### Observation

Five colored lines correspond to the top-5 pages as α increases from 0.5 to 0.95:

- **All five lines increase monotonically** with α → larger α boosts the scores of important pages.
- **P03649 (red)** remains highest with the steepest slope → it benefits the most from link structure.
- **The gap between P03649 and P02204 (purple)** widens as α grows → larger α **amplifies inequality** between hubs and ordinary pages.
- At α = 0.50: scores range from 0.0017 to 0.0035 (narrow gap).
- At α = 0.95: scores range from 0.0019 to 0.0047 (~50% wider gap).

### Comment — Role of α

| α | Meaning | Consequence |
|---|---------|--------|
| Low (0.5) | Random-jump probability is 50% | Uniform scores, fast convergence (17 iters), poor discrimination |
| Medium (0.85) | Balanced link-following and teleport | Scores match real importance, 29 iterations |
| High (0.95) | Link structure dominates 95% | Hubs maximally amplified, slower convergence (35 iters) |

**The top-5 ranking order does not change** across the entire α range — confirming that graph structure, not α, is the dominant ranking factor.

---

## 4. Spearman Correlation Matrix Across α (Bottom-right figure)

### Observation

A 6×6 matrix over α ∈ {0.50, 0.65, 0.75, 0.85, 0.90, 0.95}:

| | 0.50 | 0.65 | 0.75 | 0.85 | 0.90 | 0.95 |
|--|--|--|--|--|--|--|
| **0.50** | 1.000 | 0.996 | 0.998 | 0.995 | 0.995 | 0.992 |
| **0.65** | 0.996 | 1.000 | 0.998 | 0.997 | 0.996 | 0.991 |
| **0.75** | 0.998 | 0.998 | 1.000 | 0.998 | 0.998 | 0.993 |
| **0.85** | 0.995 | 0.997 | 0.998 | 1.000 | 0.999 | 0.992 |
| **0.90** | 0.995 | 0.996 | 0.998 | 0.999 | 1.000 | 0.992 |
| **0.95** | 0.992 | 0.991 | 0.993 | 0.992 | 0.992 | 1.000 |

The entire matrix is dark green — the minimum correlation is **ρ = 0.991** (between α=0.65 and α=0.95).

### Comment — Ranking Robustness

The result is unambiguous:

1. **PageRank rankings are extremely robust** to variation of α across [0.50, 0.95].
2. Correlations near 1 demonstrate that **the in-link structure of the graph is the dominant factor**, not the choice of α.
3. The farthest α pair (0.50 and 0.95) still yields ρ = 0.992 — **rankings differ only marginally**.
4. For real data (wiki-Vote), α ∈ **0.75 – 0.90 is the safe zone** for the most stable results (mutual correlation ≥ 0.998).

---

## 5. Summary — Synthetic vs. wiki-Vote

| Criterion | Synthetic (150 pages) | wiki-Vote (7,115 pages) |
|---|---|---|
| Score distribution | Mild power-law | Stronger power-law |
| Score of page #1 | 0.0243 | 0.0046 |
| Gap #1 vs #20 | ~2.7× | ~2.5× |
| Iterations (α=0.85) | 31 | 29 |
| α-stability | ρ ≥ 0.986 | ρ ≥ 0.992 |
| Dangling nodes | 0 | 1,005 (14.1%) |

The real graph has **higher ρ** than the synthetic one — indicating that wiki-Vote has a stronger and more consistent hub-authority structure that is less affected by α.

---

## 6. Conclusion

**On the wiki-Vote dataset:**
- The Wikipedia voting network exhibits all hallmarks of a real web graph: power-law distribution, hub dominance, a long tail of low-rank nodes.
- P03649 is the most influential user — the one most broadly trusted by the community.

**On the PageRank algorithm:**
- Power Iteration converges in just **29 iterations** over 7,115 nodes — confirming the efficiency of the O(|E|) sparse implementation.
- The Google matrix G = αP + (1-α)(1/n)ee^T guarantees unique convergence by the Perron-Frobenius theorem, even with 1,005 dangling nodes.
- α = 0.85 is the optimal balance between convergence speed and discrimination quality.

**Practical implication:**
- PageRank rankings can be **trusted independently of the choice of α** — Spearman correlation > 0.99 across the entire range α ∈ [0.5, 0.95].
- Link structure (who voted for whom) is the decisive ranking factor, not the model parameter.
