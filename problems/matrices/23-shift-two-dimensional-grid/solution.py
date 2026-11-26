class Solution:
    def shiftGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m, n = len(grid), len(grid[0])
        size = m*n; shift = k % size
        flat = [x for row in grid for x in row]
        flat = flat[-shift:] + flat[:-shift] if shift else flat
        return [flat[r*n:(r+1)*n] for r in range(m)]
