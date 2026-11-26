class Solution:
    def rotateGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m, n = len(grid), len(grid[0])
        res = [row[:] for row in grid]
        layers = min(m, n) // 2
        for layer in range(layers):
            top, bottom = layer, m - 1 - layer
            left, right = layer, n - 1 - layer
            coords = []
            for c in range(left, right):
                coords.append((top, c))
            for r in range(top, bottom):
                coords.append((r, right))
            for c in range(right, left, -1):
                coords.append((bottom, c))
            for r in range(bottom, top, -1):
                coords.append((r, left))
            length = len(coords)
            shift = k % length
            for i, (r, c) in enumerate(coords):
                sr, sc = coords[(i + shift) % length]
                res[r][c] = grid[sr][sc]
        return res
