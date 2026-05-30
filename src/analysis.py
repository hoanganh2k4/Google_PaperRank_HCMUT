"""
Analysis helpers:
    spearman_rank_corr : Spearman rank correlation (custom, no scipy).
    print_table        : Pretty-print a Top-K PageRank ranking table.
"""

import numpy as np


def spearman_rank_corr(x: np.ndarray, y: np.ndarray) -> float:
    """
    Spearman rank correlation:

        ρ = 1 - 6·Σd² / (n·(n²-1))

    where d_i = rank(x_i) - rank(y_i). Implemented manually, no scipy.
    """
    n  = len(x)
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    d2 = np.sum((rx - ry) ** 2)
    return 1.0 - 6.0 * d2 / (n * (n ** 2 - 1))


def print_table(pi: np.ndarray,
                pages: list[str],
                title: str = "PageRank",
                top_k: int = 20,
                page_cat: dict | None = None):
    """Print a Top-K ranking table sorted by descending score."""
    ranked = sorted(enumerate(pi), key=lambda x: -x[1])
    w = 70
    print(f"\n{'═' * w}")
    print(f"  {title}")
    print(f"{'═' * w}")
    header = f"{'Rank':<5} {'Page':<12} {'Score':<14} {'Percentile':>10}"
    if page_cat:
        header += "  Topic"
    print(header)
    print(f"{'─' * w}")
    for rank, (idx, score) in enumerate(ranked[:top_k], 1):
        pct = 100.0 * (len(pi) - rank) / len(pi)
        row = f"{rank:<5} {pages[idx]:<12} {score:<14.8f} {pct:>9.1f}%"
        if page_cat:
            row += f"  {page_cat.get(idx, '-')}"
        print(row)
    print(f"{'─' * w}")
    print(f"  Total {len(pi)} pages | Σ scores = {pi.sum():.8f}")
