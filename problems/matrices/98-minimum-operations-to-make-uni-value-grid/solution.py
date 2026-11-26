class Solution:
    def minOperationsUniValue(self, grid: List[List[int]], x: int) -> int:
        rem = grid[0][0] % x
        vals = []
        for row in grid:
            for v in row:
                if v % x != rem:
                    return -1
                vals.append(v)
        vals.sort()
        med = vals[len(vals) // 2]
        return sum(abs(v - med) // x for v in vals)
