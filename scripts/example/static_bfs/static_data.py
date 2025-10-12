import random
from typing import Dict, List, Tuple

class StaticGraphGenER:
    """
    Erdős–Rényi G(N, p) static graph generator (undirected).
    Returns:
      info = {
        'N': int,
        'edges': List[Tuple[int,int]],  # u < v
        'adj': Dict[int, List[int]]     # neighbors sorted asc
      }
    """
    def sample_graph(self, N: int = 10, p: float = 0.2, seed: int = 0):
        rng = random.Random(seed)
        edges: List[Tuple[int, int]] = []
        for u in range(N):
            for v in range(u + 1, N):
                if rng.random() < p:
                    edges.append((u, v))
        adj: Dict[int, List[int]] = {i: [] for i in range(N)}
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        for i in range(N):
            adj[i].sort()
        return {'N': N, 'edges': edges, 'adj': adj}

