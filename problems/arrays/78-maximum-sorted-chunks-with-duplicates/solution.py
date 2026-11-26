class Solution:
    def maxChunksToSortedWithDuplicates(self, arr: List[int]) -> int:
        suffix = [0] * len(arr)
        suffix[-1] = arr[-1]
        for i in range(len(arr) - 2, -1, -1): suffix[i] = min(arr[i], suffix[i + 1])
        chunks = 1
        high = arr[0]
        for i in range(len(arr) - 1):
            high = max(high, arr[i])
            if high <= suffix[i + 1]: chunks += 1
        return chunks
