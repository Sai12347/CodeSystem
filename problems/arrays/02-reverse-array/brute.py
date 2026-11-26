class Solution:
    def reverseArray(self, nums: List[int]) -> None:
        nums[:] = [nums[i] for i in range(len(nums) - 1, -1, -1)]
