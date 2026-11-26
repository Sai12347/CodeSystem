class Solution:
    def distanceLimitedPathsExist(
        self, n: int, edgeList: List[List[int]], queries: List[List[int]]
    ) -> List[bool]:
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1

        edges = sorted(edgeList, key=lambda e: e[2])
        order = sorted(range(len(queries)), key=lambda i: queries[i][2])

        ans = [False] * len(queries)
        ei = 0
        m = len(edges)
        for qi in order:
            p, q, limit = queries[qi]
            while ei < m and edges[ei][2] < limit:
                union(edges[ei][0], edges[ei][1])
                ei += 1
            ans[qi] = find(p) == find(q)

        return ans
