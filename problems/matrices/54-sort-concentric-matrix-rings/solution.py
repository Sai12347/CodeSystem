class Solution:
    def sortMatrixRings(self, grid: List[List[int]]) -> List[List[int]]:
        m, n = len(grid), len(grid[0])
        res = [[0] * n for _ in range(m)]
        top, bottom, left, right = 0, m - 1, 0, n - 1
        while top <= bottom and left <= right:
            coords = []
            for c in range(left, right + 1):
                coords.append((top, c))
            for r in range(top + 1, bottom + 1):
                coords.append((r, right))
            if bottom > top and right > left:
                for c in range(right - 1, left - 1, -1):
                    coords.append((bottom, c))
                for r in range(bottom - 1, top, -1):
                    coords.append((r, left))
            vals = sorted(grid[r][c] for r, c in coords)
            for (r, c), v in zip(coords, vals):
                res[r][c] = v
            top += 1
            bottom -= 1
            left += 1
            right -= 1
        return res
