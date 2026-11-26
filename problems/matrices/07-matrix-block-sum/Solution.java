class Solution {
    public int[][] matrixBlockSum(int[][] mat, int k) {
        int m = mat.length, n = mat[0].length;
        int[][] pref = new int[m + 1][n + 1];
        for (int r = 0; r < m; r++) {
            int rowSum = 0;
            for (int c = 0; c < n; c++) {
                rowSum += mat[r][c];
                pref[r + 1][c + 1] = pref[r][c + 1] + rowSum;
            }
        }
        int[][] ans = new int[m][n];
        for (int r = 0; r < m; r++) {
            int r1 = Math.max(0, r - k);
            int r2 = Math.min(m - 1, r + k);
            for (int c = 0; c < n; c++) {
                int c1 = Math.max(0, c - k);
                int c2 = Math.min(n - 1, c + k);
                ans[r][c] = pref[r2 + 1][c2 + 1]
                    - pref[r1][c2 + 1]
                    - pref[r2 + 1][c1]
                    + pref[r1][c1];
            }
        }
        return ans;
    }
}
