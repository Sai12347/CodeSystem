class Solution:
    def findUnsortedSubarray(self, nums: List[int]) -> int:
        target = sorted(nums)
        left, right = -1, -1
        for i, (a, b) in enumerate(zip(nums, target)):
            if a != b:
                if left == -1:
                    left = i
                right = i
        return 0 if left == -1 else right - left + 1
