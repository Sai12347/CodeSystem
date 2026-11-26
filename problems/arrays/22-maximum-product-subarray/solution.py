class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        high = low = best = nums[0]
        for x in nums[1:]:
            if x < 0:
                high, low = low, high
            high = max(x, high * x)
            low = min(x, low * x)
            best = max(best, high)
        return best
