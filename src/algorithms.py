"""
Core PageRank algorithms: Power Iteration in dense and sparse form.

Both solve the eigenvector equation π = G·π by iterating
    π(k+1) = G · π(k)
until ||π(k+1) - π(k)||_1 < tol.
"""

import numpy as np

from .graph import WebGraph


def pagerank_power_iteration(G: np.ndarray,
                              tol: float = 1e-10,
                              max_iter: int = 1000) -> tuple:
    """
    Power Iteration on the full matrix G (used for verification).

        π(k+1) = G · π(k)        until ||π(k+1) - π(k)||₁ < tol

    π is the (left) eigenvector of G with eigenvalue 1. Power Iteration
    converges because |α · λ₂| < 1 for primitive G (λ₂ < 1).

    Returns:
        (pi, iterations, converged_flag)
    """
    n = G.shape[0]
    pi = np.ones(n, dtype=float) / n

    for k in range(1, max_iter + 1):
        pi_new = G @ pi
        pi_new /= pi_new.sum()
        if np.linalg.norm(pi_new - pi, 1) < tol:
            return pi_new, k, True
        pi = pi_new

    return pi, max_iter, False


def pagerank_sparse(graph: WebGraph,
                    alpha: float = 0.85,
                    tol: float = 1e-10,
                    max_iter: int = 1000,
                    personalization: np.ndarray | None = None) -> tuple:
    """
    Power Iteration on a sparse graph without storing an n × n matrix.
    Cost is O(|E|) per iteration instead of O(n²); usable for large graphs.

    Explicit update with dangling-node handling:

        π(k+1) = α · [ P·π(k) + d(k)·v ] + (1 - α)·v

    where d(k) = Σ_{i dangling} π(k)[i] is the rank mass on out-degree-0 pages.

    Returns:
        (pi, iterations, converged_flag)
    """
    n = graph.n
    if personalization is None:
        v = np.ones(n, dtype=float) / n
    else:
        v = np.array(personalization, dtype=float)
        v /= v.sum()

    dangling = graph.dangling_nodes
    pi = np.ones(n, dtype=float) / n

    for k in range(1, max_iter + 1):
        pi_new = np.zeros(n, dtype=float)

        # Mass currently held on dangling nodes.
        d_mass = pi[dangling].sum() if dangling else 0.0

        # Sparse multiplication: P · pi.
        for i in range(n):
            out = graph.out_links[i]
            if out:
                contrib = pi[i] / len(out)
                for j in out:
                    pi_new[j] += contrib

        pi_new += d_mass * v
        pi_new  = alpha * pi_new + (1.0 - alpha) * v

        if np.linalg.norm(pi_new - pi, 1) < tol:
            return pi_new, k, True
        pi = pi_new

    return pi, max_iter, False
