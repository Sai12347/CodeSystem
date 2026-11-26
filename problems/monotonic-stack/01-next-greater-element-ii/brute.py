class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [-1] * n
        for i in range(n):
            for step in range(1, n):
                val = nums[(i + step) % n]
                if val > nums[i]:
                    res[i] = val
                    break
        return res
