class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        def rob_range(start: int, end: int) -> int:
            prev2 = 0
            prev1 = 0
            for i in range(start, end):
                prev2, prev1 = prev1, max(prev1, prev2 + nums[i])
            return prev1

        return max(rob_range(0, len(nums) - 1), rob_range(1, len(nums)))
