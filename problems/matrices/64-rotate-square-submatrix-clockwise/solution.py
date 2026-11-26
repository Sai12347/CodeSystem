class Solution:
    def rotateSubmatrix(self, grid: List[List[int]], row: int, col: int, k: int, turns: int) -> List[List[int]]:
        res = [r[:] for r in grid]
        t = turns % 4
        if t == 0 or k == 1:
            return res
        for dr in range(k):
            for dc in range(k):
                val = grid[row + dr][col + dc]
                if t == 1:
                    res[row + dc][col + k - 1 - dr] = val
                elif t == 2:
                    res[row + k - 1 - dr][col + k - 1 - dc] = val
                else:
                    res[row + k - 1 - dc][col + dr] = val
        return res
