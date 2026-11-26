class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        rows, cols = len(heights), len(heights[0])
        inf = 10**9
        effort = [[inf] * cols for _ in range(rows)]
        effort[0][0] = 0
        heap = [(0, 0, 0)]

        while heap:
            e, r, c = heapq.heappop(heap)
            if e > effort[r][c]:
                continue
            if r == rows - 1 and c == cols - 1:
                return e
            h = heights[r][c]
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < rows and 0 <= nc < cols:
                    ne = max(e, abs(h - heights[nr][nc]))
                    if ne < effort[nr][nc]:
                        effort[nr][nc] = ne
                        heapq.heappush(heap, (ne, nr, nc))

        return effort[rows - 1][cols - 1]
