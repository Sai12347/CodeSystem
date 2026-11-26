class Solution:
    def findBall(self, grid: List[List[int]]) -> List[int]:
        m, n = len(grid), len(grid[0])
        ans = [-1] * n
        for start in range(n):
            col = start
            for r in range(m):
                d = grid[r][col]
                nxt = col + d
                if nxt < 0 or nxt >= n or grid[r][nxt] != d:
                    col = -1
                    break
                col = nxt
            ans[start] = col
        return ans
