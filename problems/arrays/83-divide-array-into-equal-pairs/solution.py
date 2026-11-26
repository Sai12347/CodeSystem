class Solution:
    def canDivideIntoPairs(self, nums: List[int]) -> int:
        counts = [0] * 501
        for x in nums: counts[x] ^= 1
        return not any(counts)
