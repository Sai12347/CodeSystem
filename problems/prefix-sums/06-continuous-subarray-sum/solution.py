class Solution:
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        first_seen = {0: -1}
        prefix = 0
        for i, x in enumerate(nums):
            prefix = (prefix + x) % k
            if prefix in first_seen:
                if i - first_seen[prefix] >= 2:
                    return True
            else:
                first_seen[prefix] = i
        return False
