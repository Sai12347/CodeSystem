class Solution:
    def numberOfSubarrays(self, nums: List[int], k: int) -> int:
        def at_most(goal: int) -> int:
            if goal < 0:
                return 0
            left = 0
            odds = 0
            total = 0
            for right, val in enumerate(nums):
                odds += val & 1
                while odds > goal:
                    odds -= nums[left] & 1
                    left += 1
                total += right - left + 1
            return total

        return at_most(k) - at_most(k - 1)
