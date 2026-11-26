class Solution:
    def minOperationsToDivisible(self, nums: List[int], k: int) -> int:
        return sum(nums) % k
