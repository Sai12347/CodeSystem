class Solution {
    public int maxSideLength(int[][] mat, int threshold) {
        int m = mat.length, n = mat[0].length;
        int[][] pref = new int[m + 1][n + 1];
        int best = 0;
        for (int r = 1; r <= m; r++) {
            for (int c = 1; c <= n; c++) {
                pref[r][c] = mat[r - 1][c - 1] + pref[r - 1][c] + pref[r][c - 1] - pref[r - 1][c - 1];
                int k = best + 1;
                if (r >= k && c >= k) {
                    int sq = pref[r][c] - pref[r - k][c] - pref[r][c - k] + pref[r - k][c - k];
                    if (sq <= threshold) best = k;
                }
            }
        }
        return best;
    }
}
