class Solution:
    def maxChunksToSorted(self, nums: List[int]) -> int:
        chunks = high = 0
        for i, x in enumerate(nums):
            high = max(high, x)
            if high == i:
                chunks += 1
        return chunks
