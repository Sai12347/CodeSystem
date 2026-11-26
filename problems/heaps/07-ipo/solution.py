class Solution:
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        projects = sorted(zip(capital, profits))
        max_heap = []
        idx = 0
        n = len(projects)
        for _ in range(min(k, n)):
            while idx < n and projects[idx][0] <= w:
                heapq.heappush(max_heap, -projects[idx][1])
                idx += 1
            if not max_heap:
                break
            w -= heapq.heappop(max_heap)
        return w
