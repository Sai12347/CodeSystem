class Solution:
    def diagonalSort(self, mat: List[List[int]]) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        res = [row[:] for row in mat]
        starts = [(r, 0) for r in range(m)] + [(0, c) for c in range(1, n)]
        for sr, sc in starts:
            vals = []
            r, c = sr, sc
            while r < m and c < n:
                vals.append(res[r][c])
                r += 1
                c += 1
            vals.sort()
            r, c = sr, sc
            for v in vals:
                res[r][c] = v
                r += 1
                c += 1
        return res
