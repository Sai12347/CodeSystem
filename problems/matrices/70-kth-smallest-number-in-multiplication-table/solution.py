class Solution:
    def findKthNumber(self, m: int, n: int, k: int) -> int:
        if m > n:
            m, n = n, m
        lo, hi = 1, m * n
        while lo < hi:
            mid = (lo + hi) // 2
            cnt = 0
            for i in range(1, m + 1):
                q = mid // i
                if q == 0:
                    break
                cnt += n if q > n else q
            if cnt >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo
