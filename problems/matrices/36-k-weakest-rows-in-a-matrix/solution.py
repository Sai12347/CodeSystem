class Solution:
    def kWeakestRows(self, mat: List[List[int]], k: int) -> List[int]:
        m, n = len(mat), len(mat[0])
        strengths = []
        for r in range(m):
            row = mat[r]
            lo, hi = 0, n
            while lo < hi:
                mid = (lo + hi) // 2
                if row[mid] == 1:
                    lo = mid + 1
                else:
                    hi = mid
            strengths.append((lo, r))
        strengths.sort()
        return [r for _, r in strengths[:k]]
