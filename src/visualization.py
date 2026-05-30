"""
Save four separate result figures per dataset:
    01_score_distribution.png
    02_top20_pages.png
    03_alpha_effect.png
    04_spearman_correlation.png
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .graph import WebGraph
from .analysis import spearman_rank_corr


def plot_results(graph: WebGraph,
                 pi_std: np.ndarray,
                 alpha_results: dict,
                 out_dir: str):
    """
    Write 4 PNG figures into `out_dir`.
    All captions are in English.
    """
    os.makedirs(out_dir, exist_ok=True)
    alphas = sorted(alpha_results.keys())
    n_edges = sum(len(v) for v in graph.out_links.values())
    suptitle_suffix = f"{graph.source} ({graph.n} pages, {n_edges} edges)"

    # ----- Figure 1: Score distribution (log scale) -----
    fig, ax = plt.subplots(figsize=(8, 6))
    sorted_scores = sorted(pi_std, reverse=True)
    ax.plot(range(1, len(sorted_scores) + 1), sorted_scores, "b-", linewidth=2)
    ax.set_xlabel("Page rank")
    ax.set_ylabel("PageRank score")
    ax.set_title(f"Score Distribution (Log Scale) — {suptitle_suffix}",
                 fontsize=11, fontweight="bold")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    path1 = os.path.join(out_dir, "01_score_distribution.png")
    plt.tight_layout()
    plt.savefig(path1, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [Saved] {path1}")

    # ----- Figure 2: Top 20 pages -----
    fig, ax = plt.subplots(figsize=(8, 6))
    top_idx    = np.argsort(pi_std)[::-1][:20]
    top_scores = pi_std[top_idx]
    labels     = [graph.pages[i] for i in top_idx]

    CAT_COLOR = {
        "Technology": "steelblue", "Science": "tomato",
        "Sports": "seagreen",      "News": "goldenrod",
        "Entertainment": "mediumpurple",
    }
    colors = [CAT_COLOR.get(graph.page_cat.get(i), "dimgray") for i in top_idx]

    ax.barh(range(20), top_scores[::-1], color=colors[::-1])
    ax.set_yticks(range(20))
    ax.set_yticklabels(labels[::-1], fontsize=8)
    ax.set_xlabel("PageRank Score")
    ax.set_title(f"Top 20 Pages — {suptitle_suffix}",
                 fontsize=11, fontweight="bold")
    ax.grid(True, alpha=0.3, axis="x")

    if graph.categories:
        from matplotlib.patches import Patch
        legend_els = [Patch(facecolor=c, label=k) for k, c in CAT_COLOR.items()]
        ax.legend(handles=legend_els, fontsize=8, loc="lower right", title="Topic")

    path2 = os.path.join(out_dir, "02_top20_pages.png")
    plt.tight_layout()
    plt.savefig(path2, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [Saved] {path2}")

    # ----- Figure 3: Effect of alpha on Top-5 pages -----
    fig, ax = plt.subplots(figsize=(8, 6))
    top5   = np.argsort(pi_std)[::-1][:5]
    colors_line = ["red", "blue", "green", "orange", "purple"]
    for idx, col in zip(top5, colors_line):
        scores_a = [alpha_results[a][idx] for a in alphas]
        ax.plot(alphas, scores_a, "o-", color=col,
                label=graph.pages[idx], linewidth=2, markersize=6)
    ax.set_xlabel("Damping factor α")
    ax.set_ylabel("PageRank Score")
    ax.set_title(f"Effect of α on Top-5 Pages — {suptitle_suffix}",
                 fontsize=11, fontweight="bold")
    ax.legend(fontsize=9, title="Page")
    ax.grid(True, alpha=0.3)
    path3 = os.path.join(out_dir, "03_alpha_effect.png")
    plt.tight_layout()
    plt.savefig(path3, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [Saved] {path3}")

    # ----- Figure 4: Spearman rank correlation matrix -----
    fig, ax = plt.subplots(figsize=(8, 6))
    m    = len(alphas)
    corr = np.zeros((m, m))
    for i, a1 in enumerate(alphas):
        for j, a2 in enumerate(alphas):
            corr[i, j] = spearman_rank_corr(alpha_results[a1], alpha_results[a2])
    im = ax.imshow(corr, cmap="RdYlGn", vmin=0.8, vmax=1.0)
    ax.set_xticks(range(m))
    ax.set_yticks(range(m))
    ax.set_xticklabels([str(a) for a in alphas], fontsize=10)
    ax.set_yticklabels([str(a) for a in alphas], fontsize=10)
    ax.set_xlabel("Damping factor α")
    ax.set_ylabel("Damping factor α")
    ax.set_title(f"Spearman Rank Correlation Between α Values — {suptitle_suffix}",
                 fontsize=11, fontweight="bold")
    plt.colorbar(im, ax=ax, label="Spearman ρ")
    for i in range(m):
        for j in range(m):
            ax.text(j, i, f"{corr[i,j]:.3f}", ha="center", va="center",
                    fontsize=9, color="black")
    path4 = os.path.join(out_dir, "04_spearman_correlation.png")
    plt.tight_layout()
    plt.savefig(path4, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [Saved] {path4}")
