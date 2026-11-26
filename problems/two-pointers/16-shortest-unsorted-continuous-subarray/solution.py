class Solution:
    def findUnsortedSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        right = -1
        max_seen = nums[0]
        for i in range(1, n):
            if nums[i] < max_seen:
                right = i
            else:
                max_seen = nums[i]

        if right == -1:
            return 0

        left = n
        min_seen = nums[-1]
        for i in range(n - 2, -1, -1):
            if nums[i] > min_seen:
                left = i
            else:
                min_seen = nums[i]

        return right - left + 1
