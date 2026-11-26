class Solution:
    def maxSumSubmatrix(self, matrix: List[List[int]], k: int) -> int:
        import bisect
        m, n = len(matrix), len(matrix[0])
        if m > n:
            matrix = [[matrix[r][c] for r in range(m)] for c in range(n)]
            m, n = n, m
        ans = -10**18
        for top in range(m):
            col_sums = [0] * n
            for bottom in range(top, m):
                row = matrix[bottom]
                for c in range(n):
                    col_sums[c] += row[c]
                # Fast-path with Kadane's algorithm
                cur = col_sums[0]
                best_k = cur
                for x in col_sums[1:]:
                    cur = x if cur < 0 else cur + x
                    if cur > best_k:
                        best_k = cur
                if best_k <= k:
                    if best_k > ans:
                        ans = best_k
                    if ans == k:
                        return k
                    continue
                prefixes = [0]
                pref = 0
                for x in col_sums:
                    pref += x
                    idx = bisect.bisect_left(prefixes, pref - k)
                    if idx < len(prefixes):
                        cand = pref - prefixes[idx]
                        if cand > ans:
                            ans = cand
                            if ans == k:
                                return k
                    bisect.insort(prefixes, pref)
        return ans
