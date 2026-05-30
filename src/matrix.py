"""
Construct the link matrix P (column-stochastic Markov matrix)
and the Google matrix G = αP + (1-α)·v·e^T.
"""

import numpy as np

from .graph import WebGraph


def build_link_matrix(graph: WebGraph) -> np.ndarray:
    """
    Build the link matrix P (column-stochastic / Markov matrix).

        P[j, i] = 1 / out_degree(i)   if link i -> j exists
                  0                    otherwise

    Dangling nodes (out_degree = 0) are distributed uniformly as 1/n
    to avoid rank sinks. P is a Markov matrix: every column sums to 1
    and all entries are non-negative.

    Use only for n <= 1000 because the full n × n matrix is stored in memory.
    """
    n = graph.n
    P = np.zeros((n, n), dtype=float)
    for i in range(n):
        out = list(graph.out_links[i])
        if out:
            prob = 1.0 / len(out)
            for j in out:
                P[j, i] = prob
        else:
            P[:, i] = 1.0 / n
    return P


def build_google_matrix(P: np.ndarray,
                        alpha: float = 0.85,
                        personalization: np.ndarray | None = None) -> np.ndarray:
    """
    Build the Google matrix:

        G = α · P + (1 - α) · v · e^T,    0 < α < 1

    where v is the personalization (teleport) vector (uniform 1/n by default).

    Interpretation of the random surfer:
      - With probability α    : follow a random hyperlink (P).
      - With probability 1-α  : teleport to any page distributed according to v.

    G is a primitive stochastic Markov matrix:
      - Irreducible : every page can reach every other page.
      - Aperiodic   : no fixed cycle.
    By the Perron–Frobenius theorem, G has a unique dominant eigenvalue 1
    and the corresponding eigenvector is the PageRank vector π.
    """
    n = P.shape[0]
    if personalization is None:
        v = np.ones(n, dtype=float) / n
    else:
        v = np.array(personalization, dtype=float)
        v /= v.sum()
    E = np.outer(v, np.ones(n))
    return alpha * P + (1.0 - alpha) * E
