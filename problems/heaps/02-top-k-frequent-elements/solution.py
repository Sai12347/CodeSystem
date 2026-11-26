class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = Counter(nums)
        heap = []
        for val, freq in counts.items():
            if len(heap) < k:
                heapq.heappush(heap, (freq, val))
            elif freq > heap[0][0]:
                heapq.heapreplace(heap, (freq, val))
        return [val for _, val in heap]
