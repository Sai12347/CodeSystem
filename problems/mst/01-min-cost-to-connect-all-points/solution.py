class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 1:
            return 0

        in_mst = [False] * n
        min_dist = [10**9] * n
        min_dist[0] = 0
        total_cost = 0

        for _ in range(n):
            u = -1
            best = 10**9
            for i in range(n):
                if not in_mst[i] and min_dist[i] < best:
                    best = min_dist[i]
                    u = i
            in_mst[u] = True
            total_cost += best
            ux, uy = points[u]
            for v in range(n):
                if not in_mst[v]:
                    d = abs(ux - points[v][0]) + abs(uy - points[v][1])
                    if d < min_dist[v]:
                        min_dist[v] = d

        return total_cost
