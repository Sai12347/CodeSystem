class Solution:
    def connectSticks(self, sticks: List[int]) -> int:
        if len(sticks) <= 1:
            return 0
        heap = list(sticks)
        heapq.heapify(heap)
        total = 0
        while len(heap) > 1:
            merged = heapq.heappop(heap) + heapq.heappop(heap)
            total += merged
            heapq.heappush(heap, merged)
        return total
