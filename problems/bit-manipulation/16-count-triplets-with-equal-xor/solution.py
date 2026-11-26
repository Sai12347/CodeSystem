class Solution:
    def countEqualXorTriplets(self, arr: List[int]) -> int:
        cnt = {0: 1}
        idx_sum = {0: 0}
        pref = 0
        ans = 0
        for m, v in enumerate(arr, 1):
            pref ^= v
            if pref in cnt:
                ans += cnt[pref] * (m - 1) - idx_sum[pref]
                cnt[pref] += 1
                idx_sum[pref] += m
            else:
                cnt[pref] = 1
                idx_sum[pref] = m
        return ans
