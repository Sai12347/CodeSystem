class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        present = set(nums)
        for v in range(len(nums) + 1):
            if v not in present:
                return v
        return -1
