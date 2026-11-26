class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights or not heights[0]:
            return []
        rows, cols = len(heights), len(heights[0])
        res = []
        for sr in range(rows):
            for sc in range(cols):
                q = deque([(sr, sc)])
                seen = {(sr, sc)}
                reach_pac = False
                reach_atl = False
                while q and not (reach_pac and reach_atl):
                    r, c = q.popleft()
                    if r == 0 or c == 0:
                        reach_pac = True
                    if r == rows - 1 or c == cols - 1:
                        reach_atl = True
                    if reach_pac and reach_atl:
                        break
                    h = heights[r][c]
                    for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen and heights[nr][nc] <= h:
                            seen.add((nr, nc))
                            q.append((nr, nc))
                if reach_pac and reach_atl:
                    res.append([sr, sc])
        return res
