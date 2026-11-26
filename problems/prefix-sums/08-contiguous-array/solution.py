class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        first_seen = {0: -1}
        balance = 0
        best = 0
        for i, v in enumerate(nums):
            balance += 1 if v == 1 else -1
            if balance in first_seen:
                length = i - first_seen[balance]
                if length > best:
                    best = length
            else:
                first_seen[balance] = i
        return best
