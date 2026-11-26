class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        present = set(nums)
        x = 1
        while x in present:
            x += 1
        return x
