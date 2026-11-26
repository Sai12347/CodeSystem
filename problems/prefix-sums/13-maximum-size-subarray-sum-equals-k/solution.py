class Solution:
    def maxSubArrayLen(self, nums: List[int], k: int) -> int:
        first_seen = {0: -1}
        prefix = 0
        best = 0
        for i, v in enumerate(nums):
            prefix += v
            need = prefix - k
            if need in first_seen:
                length = i - first_seen[need]
                if length > best:
                    best = length
            if prefix not in first_seen:
                first_seen[prefix] = i
        return best
