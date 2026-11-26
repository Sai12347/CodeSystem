class Solution:
    def arrayNesting(self, nums: List[int]) -> int:
        seen = [False] * len(nums)
        best = 0
        for start in range(len(nums)):
            length = 0
            i = start
            while not seen[i]:
                seen[i] = True
                length += 1
                i = nums[i]
            best = max(best, length)
        return best
