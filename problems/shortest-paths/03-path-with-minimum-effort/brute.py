class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        # Independent cross-check: binary search on answer + BFS reachability
        rows, cols = len(heights), len(heights[0])
        if rows == 1 and cols == 1:
            return 0

        def can_reach(limit: int) -> bool:
            seen = [[False] * cols for _ in range(rows)]
            seen[0][0] = True
            q = deque([(0, 0)])
            while q:
                r, c = q.popleft()
                if r == rows - 1 and c == cols - 1:
                    return True
                h = heights[r][c]
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc]:
                        if abs(h - heights[nr][nc]) <= limit:
                            seen[nr][nc] = True
                            q.append((nr, nc))
            return False

        lo, hi = 0, 10**6
        while lo < hi:
            mid = (lo + hi) // 2
            if can_reach(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
