class Solution:
    def findMinMax(self, nums: List[int]) -> List[int]:
        mn = mx = nums[0]
        for x in nums[1:]:
            if x < mn:
                mn = x
            elif x > mx:
                mx = x
        return [mn, mx]
