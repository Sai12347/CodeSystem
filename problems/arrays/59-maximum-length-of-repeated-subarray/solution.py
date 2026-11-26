class Solution:
    def findLength(self, nums1: List[int], nums2: List[int]) -> int:
        if len(nums2) > len(nums1): nums1, nums2 = nums2, nums1
        dp = [0] * (len(nums2) + 1)
        best = 0
        for x in nums1:
            for j in range(len(nums2) - 1, -1, -1):
                dp[j + 1] = dp[j] + 1 if x == nums2[j] else 0
                best = max(best, dp[j + 1])
        return best
