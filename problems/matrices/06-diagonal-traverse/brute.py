class Solution:
    def findDiagonalOrder(self, mat: List[List[int]]) -> List[int]:
        m, n = len(mat), len(mat[0])
        buckets = [[] for _ in range(m + n - 1)]
        for r in range(m):
            for c in range(n):
                buckets[r + c].append(mat[r][c])
        res = []
        for d, vals in enumerate(buckets):
            if d % 2 == 0:
                res.extend(reversed(vals))
            else:
                res.extend(vals)
        return res
