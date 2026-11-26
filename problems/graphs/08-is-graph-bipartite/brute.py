class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        # Independent Union-Find check: for every edge (u, v), u and v must lie
        # in opposite partitions, so u's neighbors are all unioned together.
        n = len(graph)
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        for u, nbrs in enumerate(graph):
            if not nbrs:
                continue
            ru = find(u)
            first = nbrs[0]
            for v in nbrs:
                if find(v) == ru:
                    return False
                union(first, v)
        return True
