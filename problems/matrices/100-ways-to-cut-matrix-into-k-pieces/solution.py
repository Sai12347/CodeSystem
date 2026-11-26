class Solution:
    def waysToCutMatrix(self, grid: List[str], k: int) -> int:
        MOD = 1_000_000_007
        m, n = len(grid), len(grid[0])
        apples = [[0] * (n + 1) for _ in range(m + 1)]
        for r in range(m - 1, -1, -1):
            for c in range(n - 1, -1, -1):
                apples[r][c] = (
                    (1 if grid[r][c] == "A" else 0)
                    + apples[r + 1][c]
                    + apples[r][c + 1]
                    - apples[r + 1][c + 1]
                )
        dp = [[1 if apples[r][c] > 0 else 0 for c in range(n)] for r in range(m)]
        for _ in range(2, k + 1):
            nxt = [[0] * n for _ in range(m)]
            for r in range(m):
                for c in range(n):
                    tot_here = apples[r][c]
                    if tot_here == 0:
                        continue
                    ways = 0
                    for nr in range(r + 1, m):
                        if tot_here - apples[nr][c] > 0:
                            ways += dp[nr][c]
                    for nc in range(c + 1, n):
                        if tot_here - apples[r][nc] > 0:
                            ways += dp[r][nc]
                    nxt[r][c] = ways % MOD
            dp = nxt
        return dp[0][0]
