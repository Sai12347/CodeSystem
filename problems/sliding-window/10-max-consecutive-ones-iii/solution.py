class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        left = 0
        zeros = 0
        best = 0
        for right, val in enumerate(nums):
            if val == 0:
                zeros += 1
            while zeros > k:
                if nums[left] == 0:
                    zeros -= 1
                left += 1
            length = right - left + 1
            if length > best:
                best = length
        return best
