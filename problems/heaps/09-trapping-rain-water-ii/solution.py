class Solution:
    def trapRainWater(self, heightMap: List[List[int]]) -> int:
        m, n = len(heightMap), len(heightMap[0])
        if m <= 2 or n <= 2:
            return 0
        visited = [[False] * n for _ in range(m)]
        heap = []
        for r in range(m):
            for c in (0, n - 1):
                visited[r][c] = True
                heap.append((heightMap[r][c], r, c))
        for c in range(1, n - 1):
            for r in (0, m - 1):
                visited[r][c] = True
                heap.append((heightMap[r][c], r, c))
        heapq.heapify(heap)

        water = 0
        dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
        while heap:
            h, r, c = heapq.heappop(heap)
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and not visited[nr][nc]:
                    visited[nr][nc] = True
                    nh = heightMap[nr][nc]
                    if nh < h:
                        water += h - nh
                        heapq.heappush(heap, (h, nr, nc))
                    else:
                        heapq.heappush(heap, (nh, nr, nc))
        return water
