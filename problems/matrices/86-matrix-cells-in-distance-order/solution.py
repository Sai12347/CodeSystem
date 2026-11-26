class Solution:
    def allCellsDistOrder(self, rows: int, cols: int, rCenter: int, cCenter: int) -> List[List[int]]:
        max_d = max(rCenter, rows - 1 - rCenter) + max(cCenter, cols - 1 - cCenter)
        buckets = [[] for _ in range(max_d + 1)]
        for r in range(rows):
            dr = abs(r - rCenter)
            for c in range(cols):
                buckets[dr + abs(c - cCenter)].append([r, c])
        res = []
        for b in buckets:
            res.extend(b)
        return res
