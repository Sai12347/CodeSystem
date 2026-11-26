class Solution:
    def allocatePages(self, pages: List[int], students: int) -> int:
        n = len(pages)
        if students > n:
            return -1
        if n <= 60:
            pref = [0] * (n + 1)
            for i, p in enumerate(pages):
                pref[i + 1] = pref[i] + p
            INF = 10**18
            dp = [INF] * (n + 1)
            dp[0] = 0
            for _ in range(students):
                ndp = [INF] * (n + 1)
                for i in range(1, n + 1):
                    best = INF
                    for j in range(i):
                        val = dp[j] if dp[j] > pref[i] - pref[j] else pref[i] - pref[j]
                        if val < best:
                            best = val
                    ndp[i] = best
                dp = ndp
            return dp[n]

        lo, hi = max(pages), sum(pages)
        while lo < hi:
            mid = (lo + hi) // 2
            cnt, cur = 1, 0
            for p in pages:
                if cur + p > mid:
                    cnt += 1
                    cur = p
                else:
                    cur += p
            if cnt <= students:
                hi = mid
            else:
                lo = mid + 1
        return lo
