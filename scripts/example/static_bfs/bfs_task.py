from typing import Dict, List

def _bfs_order(adj: Dict[int, List[int]], start: int = 0) -> List[int]:
    """Deterministic BFS: neighbors in ascending order; covers disconnected graphs."""
    N = len(adj)
    visited = [False] * N
    order: List[int] = []
    q: List[int] = []

    def push(s: int):
        visited[s] = True
        q.append(s)

    push(start)
    head = 0
    while True:
        while head < len(q):
            u = q[head]; head += 1
            order.append(u)
            for v in adj[u]:
                if not visited[v]:
                    push(v)
        # next component (smallest unvisited)
        nxt = -1
        for i in range(N):
            if not visited[i]:
                nxt = i
                break
        if nxt == -1:
            break
        push(nxt)
    return order

class BFSOrderTask:
    """
    Task to produce BFS traversal of a static graph.
    API: generate_qa(info) -> {'problem':..., 'answer':...}
         evaluate(qa, model_output) -> metrics dict
    """
    def __init__(self, start: int = 0):
        self.start = start

    def generate_qa(self, info):
        adj = info['adj']
        gt = _bfs_order(adj, self.start)
        answer = " ".join(map(str, gt))
        problem = {
            'N': info['N'],
            'adj': adj,
            'start': self.start
        }
        return {'problem': problem, 'answer': answer}

    def evaluate(self, qa, model_output: str):
        """
        Exact sequence match after extracting integers from model output.
        Tolerates commas/newlines/extra text.
        """
        import re
        gt = qa['answer'].strip().replace(",", " ")
        pred = (model_output or "").strip().lower()
        nums = re.findall(r"-?\d+", pred)
        pred_seq = " ".join(nums)
        ok = (pred_seq == gt)
        return {'exact_match': float(ok), 'pred_seq': pred_seq, 'gt': gt}

