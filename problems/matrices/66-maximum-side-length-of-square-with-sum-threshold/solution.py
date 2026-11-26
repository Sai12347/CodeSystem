class Solution:
    def maxSideLength(self, mat: List[List[int]], threshold: int) -> int:
        m, n = len(mat), len(mat[0])
        pref = [[0] * (n + 1) for _ in range(m + 1)]
        best = 0
        for r in range(1, m + 1):
            row = mat[r - 1]
            pr = pref[r]
            pr_prev = pref[r - 1]
            for c in range(1, n + 1):
                pr[c] = row[c - 1] + pr_prev[c] + pr[c - 1] - pr_prev[c - 1]
                k = best + 1
                if r >= k and c >= k:
                    sq = pr[c] - pref[r - k][c] - pr[c - k] + pref[r - k][c - k]
                    if sq <= threshold:
                        best = k
        return best
