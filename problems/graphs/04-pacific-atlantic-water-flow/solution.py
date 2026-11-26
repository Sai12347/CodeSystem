class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights or not heights[0]:
            return []
        rows, cols = len(heights), len(heights[0])

        def bfs(starts):
            vis = [[False] * cols for _ in range(rows)]
            q = deque()
            for r, c in starts:
                if not vis[r][c]:
                    vis[r][c] = True
                    q.append((r, c))
            while q:
                r, c = q.popleft()
                h = heights[r][c]
                if r > 0 and not vis[r - 1][c] and heights[r - 1][c] >= h:
                    vis[r - 1][c] = True
                    q.append((r - 1, c))
                if r + 1 < rows and not vis[r + 1][c] and heights[r + 1][c] >= h:
                    vis[r + 1][c] = True
                    q.append((r + 1, c))
                if c > 0 and not vis[r][c - 1] and heights[r][c - 1] >= h:
                    vis[r][c - 1] = True
                    q.append((r, c - 1))
                if c + 1 < cols and not vis[r][c + 1] and heights[r][c + 1] >= h:
                    vis[r][c + 1] = True
                    q.append((r, c + 1))
            return vis

        pac_starts = [(0, c) for c in range(cols)] + [(r, 0) for r in range(rows)]
        atl_starts = [(rows - 1, c) for c in range(cols)] + [(r, cols - 1) for r in range(rows)]

        pac = bfs(pac_starts)
        atl = bfs(atl_starts)

        return [[r, c] for r in range(rows) for c in range(cols) if pac[r][c] and atl[r][c]]
