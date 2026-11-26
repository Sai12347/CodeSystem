class Solution:
    def matrixMedian(self, grid: List[List[int]]) -> int:
        import bisect
        m, n = len(grid), len(grid[0])
        lo = min(row[0] for row in grid)
        hi = max(row[-1] for row in grid)
        need = (m * n + 1) // 2
        while lo < hi:
            mid = lo + (hi - lo) // 2
            cnt = 0
            for row in grid:
                cnt += bisect.bisect_right(row, mid)
            if cnt >= need:
                hi = mid
            else:
                lo = mid + 1
        return lo
