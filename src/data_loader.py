"""
Download and load real-world graph datasets from Stanford SNAP.

The SNAP edge-list format is:
    # comment lines start with '#'
    # Nodes: <n>  Edges: <m>
    <src>\t<dst>
    ...
"""

import os
import gzip
import urllib.request


SNAP_DATASETS = {
    "wiki-Vote": {
        "url":  "https://snap.stanford.edu/data/wiki-Vote.txt.gz",
        "desc": "Wikipedia voting network - 7,115 nodes, 103,689 directed edges",
    },
    "p2p-Gnutella04": {
        "url":  "https://snap.stanford.edu/data/p2p-Gnutella04.txt.gz",
        "desc": "Gnutella P2P network - 10,879 nodes, 39,994 directed edges",
    },
    "ca-GrQc": {
        "url":  "https://snap.stanford.edu/data/ca-GrQc.txt.gz",
        "desc": "Collaboration network (arxiv GR-QC) - 5,242 nodes, 28,980 edges",
    },
}

# data/ lives at the project root (sibling of src/).
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
)


def download_dataset(name: str = "wiki-Vote") -> str:
    """
    Download a SNAP dataset into DATA_DIR, decompress it, and cache it.
    Returns the path to the decompressed .txt file.
    """
    if name not in SNAP_DATASETS:
        raise KeyError(f"Unknown dataset {name!r}. Choices: {list(SNAP_DATASETS)}")

    os.makedirs(DATA_DIR, exist_ok=True)
    info     = SNAP_DATASETS[name]
    url      = info["url"]
    gz_path  = os.path.join(DATA_DIR, f"{name}.txt.gz")
    txt_path = os.path.join(DATA_DIR, f"{name}.txt")

    if os.path.exists(txt_path):
        size_mb = os.path.getsize(txt_path) / 1024 / 1024
        print(f"  [Cache] Found existing file: {txt_path} ({size_mb:.1f} MB)")
        return txt_path

    print(f"  Downloading: {url}")

    def _progress(block_num, block_size, total_size):
        if total_size > 0:
            pct = min(100, block_num * block_size * 100 // total_size)
            print(f"\r  Progress: {pct}%", end="", flush=True)

    urllib.request.urlretrieve(url, gz_path, reporthook=_progress)
    print()

    print(f"  Decompressing -> {txt_path}")
    with gzip.open(gz_path, "rb") as f_in, open(txt_path, "wb") as f_out:
        f_out.write(f_in.read())
    os.remove(gz_path)

    size_mb = os.path.getsize(txt_path) / 1024 / 1024
    print(f"  Completed ({size_mb:.1f} MB)")
    return txt_path


def load_snap_edges(txt_path: str) -> tuple[list, dict]:
    """
    Read a SNAP edge-list file.
    Returns (edges, meta):
        edges = list of (src_orig, dst_orig) integer pairs
        meta  = metadata parsed from comment lines (Nodes, Edges)
    Self-loops (src == dst) are filtered out.
    """
    edges = []
    meta  = {}
    with open(txt_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                if "Nodes:" in line and "Edges:" in line:
                    parts = line.split()
                    for i, p in enumerate(parts):
                        if p == "Nodes:":
                            meta["nodes"] = int(parts[i + 1])
                        if p == "Edges:":
                            meta["edges"] = int(parts[i + 1])
                continue
            parts = line.split()
            if len(parts) >= 2:
                src, dst = int(parts[0]), int(parts[1])
                if src != dst:
                    edges.append((src, dst))
    return edges, meta
