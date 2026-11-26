class Solution:
    def maxMinDistance(self, stalls: List[int], cows: int) -> int:
        s = sorted(stalls)

        def can_place(dist: int) -> bool:
            cnt = 1
            last = s[0]
            for x in s[1:]:
                if x - last >= dist:
                    cnt += 1
                    last = x
            return cnt >= cows

        hi = s[-1] - s[0]
        if hi <= 5000:
            for d in range(hi, 0, -1):
                if can_place(d):
                    return d
            return 1

        lo = 1
        ans = 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if can_place(mid):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return ans
