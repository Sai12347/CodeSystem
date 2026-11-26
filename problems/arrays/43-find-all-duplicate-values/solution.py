class Solution:
    def findDuplicates(self, nums: List[int]) -> List[int]:
        counts = [0] * (len(nums) + 1)
        for x in nums:
            counts[x] += 1
        return [x for x in range(1, len(counts)) if counts[x] == 2]
