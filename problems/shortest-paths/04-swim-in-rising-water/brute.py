class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        # Independent cross-check: binary search on t + BFS
        n = len(grid)
        lo = max(grid[0][0], grid[n - 1][n - 1])
        hi = n * n - 1

        def can_reach(t: int) -> bool:
            seen = [[False] * n for _ in range(n)]
            seen[0][0] = True
            q = deque([(0, 0)])
            while q:
                r, c = q.popleft()
                if r == n - 1 and c == n - 1:
                    return True
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if 0 <= nr < n and 0 <= nc < n and not seen[nr][nc] and grid[nr][nc] <= t:
                        seen[nr][nc] = True
                        q.append((nr, nc))
            return False

        while lo < hi:
            mid = (lo + hi) // 2
            if can_reach(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
