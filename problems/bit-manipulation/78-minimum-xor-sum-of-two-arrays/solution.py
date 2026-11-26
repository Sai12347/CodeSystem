class Solution:
    def minimumXorSum(self, nums1: List[int], nums2: List[int]) -> int:
        n = len(nums1)
        size = 1 << n
        INF = 10**18
        dp = [INF] * size
        dp[0] = 0
        for mask in range(1, size):
            i = mask.bit_count() - 1
            a = nums1[i]
            best = INF
            rem = mask
            while rem:
                lb = rem & -rem
                j = lb.bit_length() - 1
                cand = dp[mask ^ lb] + (a ^ nums2[j])
                if cand < best:
                    best = cand
                rem ^= lb
            dp[mask] = best
        return dp[size - 1]
