class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0
        rows, cols = len(grid), len(grid[0])
        parent = {}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    idx = r * cols + c
                    parent[idx] = idx
                    if r > 0 and grid[r - 1][c] == "1":
                        union(idx, (r - 1) * cols + c)
                    if c > 0 and grid[r][c - 1] == "1":
                        union(idx, r * cols + (c - 1))

        return len({find(x) for x in parent})
