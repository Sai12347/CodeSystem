class Solution:
    def minimumSpanningTreeWeight(self, n: int, edges: List[List[int]]) -> int:
        if n <= 1:
            return 0
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        total = 0
        used = 0
        for u, v, w in sorted(edges, key=lambda e: e[2]):
            ru, rv = find(u), find(v)
            if ru != rv:
                if rank[ru] < rank[rv]:
                    ru, rv = rv, ru
                parent[rv] = ru
                if rank[ru] == rank[rv]:
                    rank[ru] += 1
                total += w
                used += 1
                if used == n - 1:
                    return total
        return -1
