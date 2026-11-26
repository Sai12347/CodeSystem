class Solution {
    public int waysToCutMatrix(String[] grid, int k) {
        int MOD = 1_000_000_007;
        int m = grid.length, n = grid[0].length();
        int[][] apples = new int[m + 1][n + 1];
        for (int r = m - 1; r >= 0; r--) {
            for (int c = n - 1; c >= 0; c--) {
                apples[r][c] = (grid[r].charAt(c) == 'A' ? 1 : 0)
                    + apples[r + 1][c]
                    + apples[r][c + 1]
                    - apples[r + 1][c + 1];
            }
        }
        int[][] dp = new int[m][n];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                dp[r][c] = apples[r][c] > 0 ? 1 : 0;
            }
        }
        for (int pieces = 2; pieces <= k; pieces++) {
            int[][] nxt = new int[m][n];
            for (int r = 0; r < m; r++) {
                for (int c = 0; c < n; c++) {
                    int totHere = apples[r][c];
                    if (totHere == 0) continue;
                    long ways = 0;
                    for (int nr = r + 1; nr < m; nr++) {
                        if (totHere - apples[nr][c] > 0) ways += dp[nr][c];
                    }
                    for (int nc = c + 1; nc < n; nc++) {
                        if (totHere - apples[r][nc] > 0) ways += dp[r][nc];
                    }
                    nxt[r][c] = (int) (ways % MOD);
                }
            }
            dp = nxt;
        }
        return dp[0][0];
    }
}
