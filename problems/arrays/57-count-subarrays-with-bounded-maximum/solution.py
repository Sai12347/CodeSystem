class Solution:
    def numSubarrayBoundedMax(self, nums: List[int], bound: int) -> int:
        run = total = 0
        for x in nums:
            run = run + 1 if x <= bound else 0
            total += run
        return total
