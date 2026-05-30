"""
Web graph G(V, E) — directed graph model.

Two construction modes:
    WebGraph(n_pages, seed)        : synthetic 150-page graph with 5 topics.
    WebGraph.from_edges(edges, ..) : build from a real SNAP edge list.
"""

import random
from collections import defaultdict

import numpy as np


class WebGraph:
    """
    Model the web as a directed graph G(V, E).
    V is the set of web pages; E is the set of hyperlinks.

    Attributes:
        n          : number of pages
        pages      : list of page names indexed by [0, n-1]
        out_links  : dict mapping node -> set of outgoing neighbors
        categories : dict topic -> list of page indices (synthetic only)
        page_cat   : dict page index -> topic (synthetic only)
        source     : 'synthetic' or dataset name
    """

    def __init__(self, n_pages: int = 150, seed: int = 42):
        """Construct a synthetic graph with `n_pages` pages."""
        self.n = n_pages
        self.pages = [f"Page_{i:03d}" for i in range(n_pages)]
        self.out_links: dict[int, set] = defaultdict(set)
        self.categories: dict[str, list[int]] = {}
        self.page_cat:   dict[int, str]       = {}
        self.source = "synthetic"
        self._build_synthetic(seed)

    @classmethod
    def from_edges(cls, edges: list[tuple[int, int]], dataset_name: str = "real"):
        """
        Build a graph from an edge list (src, dst) with arbitrary node IDs.
        Automatically remaps node IDs to [0, n-1] for array indexing.
        """
        all_nodes = sorted(set(u for e in edges for u in e))
        remap     = {old: new for new, old in enumerate(all_nodes)}
        n         = len(all_nodes)

        obj            = cls.__new__(cls)
        obj.n          = n
        obj.pages      = [f"P{i:05d}" for i in range(n)]
        obj.out_links  = defaultdict(set)
        obj.categories = {}
        obj.page_cat   = {}
        obj.source     = dataset_name

        for src, dst in edges:
            s, d = remap[src], remap[dst]
            obj.out_links[s].add(d)

        return obj

    def _build_synthetic(self, seed: int):
        """
        Synthetic graph with 5 topics × 30 pages = 150 pages.
        Combines:
          - dense intra-topic links (k = 3..8 per page),
          - 400 sparse inter-topic links,
          - 5 hub pages (Page_000, 030, 060, 090, 120) that attract many inbound links.
        """
        random.seed(seed)
        np.random.seed(seed)
        n = self.n

        self.categories = {
            "Technology":    list(range(0,   30)),
            "Science":       list(range(30,  60)),
            "Sports":        list(range(60,  90)),
            "News":          list(range(90,  120)),
            "Entertainment": list(range(120, 150)),
        }
        for cat, members in self.categories.items():
            for m in members:
                self.page_cat[m] = cat

        # Intra-topic links (high density).
        for cat, members in self.categories.items():
            for page in members:
                k       = random.randint(3, 8)
                targets = random.sample([m for m in members if m != page],
                                        min(k, len(members) - 1))
                for t in targets:
                    self.out_links[page].add(t)

        # Cross-topic links (low density).
        for _ in range(400):
            src, dst = random.randint(0, n - 1), random.randint(0, n - 1)
            if src != dst:
                self.out_links[src].add(dst)

        # Hub pages: the first page of each topic receives many inbound links.
        hubs = [0, 30, 60, 90, 120]
        for hub in hubs:
            for i in range(n):
                if i != hub and random.random() < 0.20:
                    self.out_links[i].add(hub)

    @property
    def dangling_nodes(self) -> list[int]:
        """Nodes with no outgoing links."""
        return [i for i in range(self.n) if len(self.out_links[i]) == 0]

    def in_degree(self) -> dict[int, int]:
        """Return a dict of in-degrees per node."""
        in_deg = defaultdict(int)
        for i in range(self.n):
            for j in self.out_links[i]:
                in_deg[j] += 1
        return dict(in_deg)

    def stats(self) -> dict:
        """Summary statistics for the graph."""
        degrees = [len(self.out_links[i]) for i in range(self.n)]
        n_edges = sum(degrees)
        in_deg  = self.in_degree()
        return {
            "Data source":             self.source,
            "Number of pages (|V|)":   self.n,
            "Number of links (|E|)":   n_edges,
            "Average out-degree":      f"{np.mean(degrees):.2f}",
            "Maximum out-degree":      max(degrees),
            "Maximum in-degree":       max(in_deg.values()) if in_deg else 0,
            "Number of dangling nodes": len(self.dangling_nodes),
        }
