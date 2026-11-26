class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0
        rows, cols = len(grid), len(grid[0])
        best = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != 1:
                    continue
                grid[r][c] = 0
                stack = [(r, c)]
                area = 0
                while stack:
                    cr, cc = stack.pop()
                    area += 1
                    if cr > 0 and grid[cr - 1][cc] == 1:
                        grid[cr - 1][cc] = 0
                        stack.append((cr - 1, cc))
                    if cr + 1 < rows and grid[cr + 1][cc] == 1:
                        grid[cr + 1][cc] = 0
                        stack.append((cr + 1, cc))
                    if cc > 0 and grid[cr][cc - 1] == 1:
                        grid[cr][cc - 1] = 0
                        stack.append((cr, cc - 1))
                    if cc + 1 < cols and grid[cr][cc + 1] == 1:
                        grid[cr][cc + 1] = 0
                        stack.append((cr, cc + 1))
                if area > best:
                    best = area

        return best
