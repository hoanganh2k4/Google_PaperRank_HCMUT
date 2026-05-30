"""
PageRank variants:
    Personalized PageRank      (Page & Brin, 1999)
    Topic-Sensitive PageRank   (Haveliwala, 2002)
    Weighted PageRank          (Xing & Ghorbani, 2004)

All three modify either the teleportation vector v or the link weights
used in the iteration, while keeping the same Power-Iteration solver.
"""

from collections import defaultdict

import numpy as np

from .graph import WebGraph
from .algorithms import pagerank_sparse


def personalized_pagerank(graph: WebGraph,
                          seed_pages: list[int],
                          alpha: float = 0.85,
                          tol: float = 1e-10) -> tuple:
    """
    Personalized PageRank (PPR).
    The teleportation vector is concentrated on `seed_pages` instead of
    being uniform. Used to bias rankings toward a user's interests.

        v[i] = 1/|seed|   if i ∈ seed_pages
        v[i] = 0          otherwise
    """
    v = np.zeros(graph.n, dtype=float)
    for p in seed_pages:
        v[p] = 1.0
    v /= v.sum()
    return pagerank_sparse(graph, alpha=alpha, tol=tol, personalization=v)


def topic_sensitive_pagerank(graph: WebGraph,
                             topics: dict[str, list[int]],
                             alpha: float = 0.85,
                             tol: float = 1e-10,
                             query_topic: str | None = None) -> tuple:
    """
    Topic-Sensitive PageRank (Haveliwala 2002).
    Precompute one PageRank vector π_t per topic t. At query time, return
    π_t for the requested topic. No user history is required while rankings
    remain context-sensitive.

    Returns:
        (pi_for_query_topic_or_combined, dict_topic -> pi_t)
    """
    topic_prs = {}
    for topic, pages in topics.items():
        v = np.zeros(graph.n, dtype=float)
        for p in pages:
            v[p] = 1.0
        v /= v.sum()
        pi_t, _, _ = pagerank_sparse(graph, alpha=alpha, tol=tol, personalization=v)
        topic_prs[topic] = pi_t

    if query_topic and query_topic in topic_prs:
        return topic_prs[query_topic], topic_prs

    combined = np.mean(list(topic_prs.values()), axis=0)
    combined /= combined.sum()
    return combined, topic_prs


def weighted_pagerank(graph: WebGraph,
                      alpha: float = 0.85,
                      tol: float = 1e-10,
                      max_iter: int = 1000) -> tuple:
    """
    Weighted PageRank (Xing & Ghorbani 2004).
    Edge weight i->j is proportional to the in-degree of j:

        W(i -> j) = in_deg(j) / Σ_{k: i->k} in_deg(k)

    Effect: pages already referenced by many other pages absorb more rank.
    Implemented as a direct sparse iteration (no dense G matrix).
    """
    n      = graph.n
    in_deg = defaultdict(int)
    for i in range(n):
        for j in graph.out_links[i]:
            in_deg[j] += 1

    v        = np.ones(n, dtype=float) / n
    dangling = graph.dangling_nodes
    pi       = np.ones(n, dtype=float) / n

    for k in range(1, max_iter + 1):
        pi_new = np.zeros(n, dtype=float)
        d_mass = pi[dangling].sum() if dangling else 0.0

        for i in range(n):
            out = list(graph.out_links[i])
            if out:
                total_in = sum(in_deg[j] for j in out)
                for j in out:
                    w = in_deg[j] / total_in if total_in > 0 else 1.0 / len(out)
                    pi_new[j] += pi[i] * w

        pi_new += d_mass * v
        pi_new  = alpha * pi_new + (1.0 - alpha) * v

        if np.linalg.norm(pi_new - pi, 1) < tol:
            return pi_new, k, True
        pi = pi_new

    return pi, max_iter, False
