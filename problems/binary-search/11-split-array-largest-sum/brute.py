class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n <= 60:
            pref = [0] * (n + 1)
            for i, x in enumerate(nums):
                pref[i + 1] = pref[i] + x
            INF = 10**18
            dp = [INF] * (n + 1)
            dp[0] = 0
            for _ in range(k):
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

        lo, hi = max(nums), sum(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            cnt, s = 1, 0
            for x in nums:
                if s + x > mid:
                    cnt += 1
                    s = x
                else:
                    s += x
            if cnt <= k:
                hi = mid
            else:
                lo = mid + 1
        return lo
