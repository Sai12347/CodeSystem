class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        visited = [[False] * n for _ in range(n)]
        visited[0][0] = True
        heap = [(grid[0][0], 0, 0)]
        ans = 0

        while heap:
            elev, r, c = heapq.heappop(heap)
            if elev > ans:
                ans = elev
            if r == n - 1 and c == n - 1:
                return ans
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
                    visited[nr][nc] = True
                    heapq.heappush(heap, (grid[nr][nc], nr, nc))

        return ans
