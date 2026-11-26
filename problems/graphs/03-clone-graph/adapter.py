from collections import deque
import solution


class Node:
    def __init__(self, val: int = 0, neighbors=None):
        self.val = int(val)
        self.neighbors = list(neighbors) if neighbors is not None else []


if not hasattr(solution, "Node"):
    solution.Node = Node


def run(inp):
    NodeCls = solution.Node
    adj = inp["adjList"]
    n = len(adj)

    orig = [NodeCls(i + 1) for i in range(n)]
    expected_orig_nbs = []
    for i, nbs in enumerate(adj):
        orig[i].neighbors = [orig[int(v) - 1] for v in nbs]
        expected_orig_nbs.append(list(orig[i].neighbors))

    orig_start = orig[0] if n > 0 else None
    orig_ids = {id(node) for node in orig}

    ans = solution.Solution().cloneGraph(orig_start)

    # Verify original graph was not modified
    for i in range(n):
        if orig[i].val != i + 1:
            return "ERROR: original graph node value was modified"
        if orig[i].neighbors is None or len(orig[i].neighbors) != len(expected_orig_nbs[i]):
            return "ERROR: original graph neighbors were modified"
        for actual_nb, exp_nb in zip(orig[i].neighbors, expected_orig_nbs[i]):
            if actual_nb is not exp_nb:
                return "ERROR: original graph neighbor reference was modified"

    if n == 0:
        if ans is not None:
            return "ERROR: expected None for empty graph"
        return []

    if ans is None:
        return "ERROR: returned None for non-empty graph"
    if id(ans) in orig_ids:
        return "ERROR: returned graph shares a node reference with the original graph"
    if ans.val != 1:
        return "ERROR: starting cloned node must have val 1"

    visited_ids = {id(ans)}
    by_val = {}
    q = deque([ans])
    while q:
        cur = q.popleft()
        if id(cur) in orig_ids:
            return "ERROR: cloned graph shares a node reference with the original graph"
        v = int(cur.val)
        if not (1 <= v <= n):
            return "ERROR: cloned node has out-of-range value"
        if v in by_val and by_val[v] is not cur:
            return "ERROR: duplicate cloned nodes created for the same value"
        by_val[v] = cur
        if cur.neighbors is None:
            return "ERROR: cloned node has None neighbors list"
        for nb in cur.neighbors:
            if nb is None:
                return "ERROR: cloned node contains a None neighbor"
            nid = id(nb)
            if nid in orig_ids:
                return "ERROR: cloned node references an original node"
            if nid not in visited_ids:
                if len(visited_ids) >= n:
                    return "ERROR: cloned graph contains more nodes than the original graph"
                visited_ids.add(nid)
                q.append(nb)

    if len(by_val) != n:
        return "ERROR: cloned graph does not contain all nodes"

    out = []
    for v in range(1, n + 1):
        nbs = sorted(int(nb.val) for nb in by_val[v].neighbors)
        out.append(nbs)
    return out
