class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        best = 0
        for x in num_set:
            if x - 1 not in num_set:
                curr = x
                while curr + 1 in num_set:
                    curr += 1
                best = max(best, curr - x + 1)
        return best
