class Solution {
    public int orderOfLargestPlusSign(int n, int[][] mines) {
        int[][] dp = new int[n][n];
        for (int[] row : dp) Arrays.fill(row, n);
        for (int[] m : mines) dp[m[0]][m[1]] = 0;

        for (int r = 0; r < n; r++) {
            int cnt = 0;
            for (int c = 0; c < n; c++) {
                cnt = (dp[r][c] == 0) ? 0 : cnt + 1;
                if (cnt < dp[r][c]) dp[r][c] = cnt;
            }
            cnt = 0;
            for (int c = n - 1; c >= 0; c--) {
                cnt = (dp[r][c] == 0) ? 0 : cnt + 1;
                if (cnt < dp[r][c]) dp[r][c] = cnt;
            }
        }
        int best = 0;
        for (int c = 0; c < n; c++) {
            int cnt = 0;
            for (int r = 0; r < n; r++) {
                cnt = (dp[r][c] == 0) ? 0 : cnt + 1;
                if (cnt < dp[r][c]) dp[r][c] = cnt;
            }
            cnt = 0;
            for (int r = n - 1; r >= 0; r--) {
                cnt = (dp[r][c] == 0) ? 0 : cnt + 1;
                if (cnt < dp[r][c]) dp[r][c] = cnt;
                if (dp[r][c] > best) best = dp[r][c];
            }
        }
        return best;
    }
}
