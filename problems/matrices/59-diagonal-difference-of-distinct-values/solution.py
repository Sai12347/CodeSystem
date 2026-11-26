class Solution:
    def differenceOfDistinctValues(self, grid: List[List[int]]) -> List[List[int]]:
        m, n = len(grid), len(grid[0])
        ans = [[0] * n for _ in range(m)]
        starts = [(0, c) for c in range(n)] + [(r, 0) for r in range(1, m)]
        for sr, sc in starts:
            cells = []
            r, c = sr, sc
            seen = set()
            while r < m and c < n:
                ans[r][c] = len(seen)
                seen.add(grid[r][c])
                cells.append((r, c))
                r += 1
                c += 1
            seen.clear()
            for r, c in reversed(cells):
                ans[r][c] = abs(ans[r][c] - len(seen))
                seen.add(grid[r][c])
        return ans
