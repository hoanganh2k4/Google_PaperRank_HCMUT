# Data Structure Evaluation — Three SNAP Datasets

This document analyzes the file format, column semantics, and statistical characteristics of the three datasets downloaded from Stanford SNAP for the PageRank experiments.

---

## 1. Common Format — SNAP Edge List

All three files follow the **SNAP edge-list format**:

```
# Comment lines start with #
# Nodes: <n>  Edges: <m>
# FromNodeId    ToNodeId
<src>   <dst>
<src>   <dst>
...
```

**Parsing rules:**
- Lines starting with `#` → skip (metadata/comments).
- Each data line contains **two integers** separated by tab: `src` and `dst`.
- Each line = **one directed edge** from node `src` to node `dst`.
- Node IDs are arbitrary integers (not necessarily contiguous from 0).
- Self-loops (`src == dst`) do not appear in these three datasets.
- **No edge weights** — binary (0/1) graph.

**How the program handles them:**
```python
# load_snap_edges() in pagerank.py
edges = []
for line in file:
    if line.startswith('#'): continue
    src, dst = map(int, line.split())
    if src != dst:
        edges.append((src, dst))

# WebGraph.from_edges() remaps to [0, n-1]
all_nodes = sorted(set(u for e in edges for u in e))
remap = {old: new for new, old in enumerate(all_nodes)}
```

---

## 2. wiki-Vote.txt

### 2.1 Header and meaning

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

**Explanation:**
- **Node** = a Wikipedia user (identified by an integer ID).
- **Edge A → B** = user A voted for B in an administrator election.
- Data collected through January 2008, covering all voting history.
- A user can cast many votes (many lines from the same `src`).
- **Vote polarity (yes/no) is not stored** — only the act of voting.

### 2.2 Structural statistics

| Metric | Value |
|---|---|
| Number of nodes | 7,115 |
| Unique edges | 103,689 |
| Duplicate edges | 0 |
| Mean out-degree | 14.57 |
| Median out-degree | **2.0** |
| Out-degree stdev | 42.28 |
| Max out-degree | **893** (node 2565) |
| Max in-degree | **457** (node 4037) |
| Dangling nodes (out=0) | 1,005 (14.1%) |
| Source-only nodes (in=0) | **4,734 (66.5%)** |
| Reciprocal edges (A→B and B→A) | 2,927 (2.8%) |

### 2.3 Out-degree distribution

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

### 2.4 Comments and interpretation

**Observation 1: Most users cast 1–2 votes, but a small minority cast hundreds.**

Mean = 14.57 but median = 2 and stdev = 42.28 — an extremely right-skewed (heavy-tailed) distribution. Node 2565 cast **893 votes** (participated in ~893 elections), while the vast majority cast only 1–2.

**Observation 2: 66.5% of nodes have in-degree = 0 — never elected.**

More than two-thirds of Wikipedia users never ran for admin, or ran but received no recorded vote. This is the "pure voters" group.

**Observation 3: Only 2.8% of edges are reciprocal — mutual voting is rare.**

The action A → B (A votes for B) almost never implies B → A. This is the characteristic of an **asymmetric voting graph** — it affects PageRank: heavy voters (high out-degree) do not necessarily receive many votes (high in-degree).

**PageRank implication:**
- High-in-degree node (node 4037: 457 votes) = the most community-trusted user.
- High-out-degree node (node 2565: 893 votes) = the most active voter, but has low PageRank because no one voted back.
- Top-5 in-degree and top-5 out-degree are **completely different sets of nodes** — demonstrating that PageRank measures "received trust" rather than "activity level".

---

## 3. p2p-Gnutella04.txt

### 3.1 Header and meaning

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

**Explanation:**
- **Node** = a computer (peer) participating in the Gnutella network on August 4, 2002.
- **Edge A → B** = peer A knows peer B's address and can send file queries to B.
- Gnutella is a first-generation P2P file-sharing network (no central server).
- Node IDs are contiguous from 0 — this is a single-time-point snapshot.

### 3.2 Structural statistics

| Metric | Value |
|---|---|
| Number of nodes | 10,876 |
| Unique edges | 39,994 |
| Duplicate edges | 0 |
| Mean out-degree | 3.68 |
| Median out-degree | **0.0** |
| Out-degree stdev | 4.92 |
| Max out-degree | **100** (node 3109) |
| Max in-degree | **72** (node 1054) |
| Dangling nodes (out=0) | **5,941 (54.6%)** |
| Source-only nodes (in=0) | 20 (0.2%) |
| Reciprocal edges | **0 (0.0%)** |

### 3.3 Out-degree distribution

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

### 3.4 Comments and interpretation

**Observation 1: Bimodal out-degree distribution — 0 or 6–10.**

This is the most prominent feature of Gnutella. Technical reason: the Gnutella protocol requires each joining peer to connect to a fixed number of other peers (typically **ultrapeers**, around 6–10 connections). Peers with insufficient capability run as **leaves** — receive only, do not forward — yielding out-degree = 0.

**Observation 2: 0% reciprocal edges — fully one-directional connections.**

Not a single (A→B, B→A) pair exists. In Gnutella, connections are not automatically bidirectional: A knowing B does not imply B knowing A. This produces a **strictly asymmetric directed graph**.

**Observation 3: 54.6% of nodes are "leaves" — receive only, do not forward.**

More than half the peers have no outbound link (out-degree = 0). These are dangling nodes — in PageRank, their rank is uniformly redistributed via teleportation rather than flowing along links. This explains why p2p-Gnutella04 converges **the fastest** (18 iterations): much of the mass is "flattened" right from the start.

**PageRank implication:**
- High-in-degree peer (node 1054: 72) = **a well-known ultrapeer**, referenced by many other peers for file lookups.
- Nodes 0, 1, 2... are connected sequentially in the snapshot → reflects the chronological order in which peers joined the network.
- "Reverse voting" is impossible (0% reciprocal) → a clear hierarchical structure (ultrapeer → leaf).

---

## 4. ca-GrQc.txt

### 4.1 Header and meaning

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
10310   3466      ← reverse edge: 10310 also coauthored with 3466
```

**Explanation:**
- **Node** = a scientist with at least one paper on arXiv in the General Relativity & Quantum Cosmology category.
- **Edge A → B** = A and B **coauthored** at least one paper.
- This is fundamentally an **undirected graph**, but SNAP stores it as directed by writing both directions:
  `A → B` and `B → A` both appear in the file.
- Node IDs are arbitrary integers (non-contiguous, broad range such as 3466, 8579, 19607...).

### 4.2 Structural statistics

| Metric | Value |
|---|---|
| Number of nodes | 5,241 |
| Unique edges | 28,968 |
| Duplicate edges | 0 |
| Mean out-degree | 5.53 |
| Median out-degree | **3.0** |
| Out-degree stdev | 7.92 |
| Max out-degree | **81** (node 21012) |
| Max in-degree | **81** (node 21012) — **same node!** |
| Dangling nodes (out=0) | **0 (0.0%)** |
| Source-only nodes (in=0) | **0 (0.0%)** |
| Reciprocal edges | **14,484 (50.0%)** |

Top-5 in-degree = Top-5 out-degree = **same 5 nodes, same values** → confirming this is a symmetric graph.

### 4.3 Out-degree distribution

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

### 4.4 Comments and interpretation

**Observation 1: Exactly 50.0% reciprocal edges — undirected graph stored as directed.**

The SNAP header says "each unordered pair of nodes is saved once" but in practice **each undirected edge is stored as 2 directed edges**. For example, edge (3466, 10310) appears in both forms:
- Line `3466 → 10310` (from node 3466's adjacency)
- Line `10310 → 3466` (from node 10310's adjacency)

This is why in-degree equals out-degree exactly for every node.

**Observation 2: No dangling node, no source-only node.**

Every scientist in the dataset has at least one collaborator in both directions. The dataset includes only the largest connected component (giant component), pruning isolated authors.

**Observation 3: Node IDs are sparse and non-contiguous (3466, 8579, 19607...).**

These are arXiv's internal IDs, not contiguous within [0, 5241]. `WebGraph.from_edges()` must remap to [0, 5240] for array indexing. This is why output shows `P00000..P05240` instead of the original IDs.

**Observation 4: Right-skewed near-normal out-degree distribution (median=3, max=81).**

There is no "super hub" as in wiki-Vote (893) or Gnutella (100). The most-collaborative scientist (node 21012) has 81 coauthors — reflecting a large research group in theoretical physics.

**PageRank implication:**
- In a symmetric graph: **PageRank ≈ Degree Centrality** — the node with the most collaborations usually leads.
- But not exactly: PageRank is a **weighted degree** via the eigenvector — a node connected to important hubs outranks one connected to leaves (e.g., P02773 beats P04281 despite equal degree).
- The second eigenvalue (λ₂) close to 1 in a symmetric network → **slow convergence** (118 iterations vs. 18–29 for the other two datasets).

---

## 5. Structural Comparison Across the Three Datasets

### 5.1 Summary table

| Feature | wiki-Vote | p2p-Gnutella04 | ca-GrQc |
|---|---|---|---|
| **Network type** | Voting (directed) | P2P file sharing (directed) | Scientific collaboration (undirected → directed) |
| **Nodes / Edges** | 7,115 / 103,689 | 10,876 / 39,994 | 5,241 / 28,968 |
| **Node ID** | Non-contiguous | Contiguous from 0 | Very sparse (arXiv IDs) |
| **Density** = 2\|E\|/\|V\|(\|V\|-1) | 0.41% | 0.034% | 0.21% |
| **Median out-degree** | 2 | **0** | 3 |
| **Out-degree stdev** | **42.28** | 4.92 | 7.92 |
| **Dangling nodes** | 14.1% | **54.6%** | **0%** |
| **Source-only (in=0)** | **66.5%** | 0.2% | 0% |
| **Reciprocal edges** | 2.8% | **0%** | **50%** |
| **PR convergence iters** | 29 | **18** | **118** |

### 5.2 Distinctive characteristics of each graph type

```
wiki-Vote:
  Highly asymmetric along the "out" direction:
  ┌─────────────────────────────────────┐
  │  Heavy voters ──→ admin hubs        │
  │  (out=893)         (in=457)         │
  │  66.5% of nodes receive no vote    │
  └─────────────────────────────────────┘
  → PageRank measures received trust, not voting activity

p2p-Gnutella04:
  Clearly tiered structure (bimodal distribution):
  ┌─────────────────────────────────────┐
  │  Leaf peers (out=0) ────→ Ultrapeer│
  │  54.6%                  (in=72)    │
  │  0% reciprocal edges               │
  └─────────────────────────────────────┘
  → PageRank measures "reachability" in the P2P network

ca-GrQc:
  Undirected graph stored as directed, fully symmetric:
  ┌─────────────────────────────────────┐
  │  A ←→ B (each collaboration = 2 edges)│
  │  in-degree ≡ out-degree             │
  │  0 dangling, 50% reciprocal         │
  └─────────────────────────────────────┘
  → PageRank ≈ Eigenvector Centrality of the undirected graph
```

### 5.3 Impact on the PageRank algorithm

| Data feature | Impact on PageRank |
|---|---|
| **High dangling (Gnutella 54.6%)** | Requires strong teleportation; converges quickly because mass is "flattened" |
| **High source-only (wiki-Vote 66.5%)** | Most nodes do not receive rank from links; rank comes mainly from (1-α)·v |
| **0% reciprocal (Gnutella)** | Tree/DAG-like structure → easy convergence, few iterations |
| **50% reciprocal (ca-GrQc)** | Symmetric network → λ₂ ≈ 1 → very slow convergence (118–374 iterations) |
| **High out-degree stdev (wiki-Vote 42.28)** | Strong power-law distribution → clear top-hub dominance |
| **Non-contiguous node IDs (ca-GrQc)** | Requires remapping to [0,n-1] before use as array indices |
