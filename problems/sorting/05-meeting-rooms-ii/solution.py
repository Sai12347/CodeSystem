class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda iv: iv[0])
        heap = []
        for s, e in intervals:
            if heap and heap[0] <= s:
                heapq.heapreplace(heap, e)
            else:
                heapq.heappush(heap, e)
        return len(heap)
