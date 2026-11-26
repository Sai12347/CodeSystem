class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 1:
            return 0
        edges = []
        for i in range(n):
            x1, y1 = points[i]
            for j in range(i + 1, n):
                edges.append((abs(x1 - points[j][0]) + abs(y1 - points[j][1]), i, j))
        edges.sort()

        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        total = 0
        used = 0
        for w, u, v in edges:
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
                    break
        return total
