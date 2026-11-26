class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        first = -1
        last = -1
        for i, val in enumerate(nums):
            if val == target:
                if first == -1:
                    first = i
                last = i
        return [first, last]
