class Solution:
    def totalHammingDistance(self, nums: List[int]) -> int:
        n = len(nums)
        total = 0
        for b in range(31):
            ones = sum((v >> b) & 1 for v in nums)
            total += ones * (n - ones)
        return total
