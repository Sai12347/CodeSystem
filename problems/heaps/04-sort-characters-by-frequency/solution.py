class Solution:
    def frequencySort(self, s: str) -> str:
        counts = Counter(s)
        max_heap = [(-freq, ch) for ch, freq in counts.items()]
        heapq.heapify(max_heap)
        parts = []
        while max_heap:
            neg_freq, ch = heapq.heappop(max_heap)
            parts.append(ch * (-neg_freq))
        return "".join(parts)
