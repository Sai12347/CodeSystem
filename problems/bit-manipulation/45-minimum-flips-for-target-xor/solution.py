class Solution:
    def minOperationsForXor(self, nums: List[int], k: int) -> int:
        diff = k
        for v in nums:
            diff ^= v
        return diff.bit_count()
