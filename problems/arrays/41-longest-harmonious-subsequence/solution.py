class Solution:
    def longestHarmoniousSubsequence(self, nums: List[int]) -> int:
        counts = Counter(nums)
        return max((counts[x] + counts[x + 1] for x in counts if x + 1 in counts), default=0)
