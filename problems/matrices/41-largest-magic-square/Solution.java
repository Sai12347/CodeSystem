class Solution {
    public int largestMagicSquare(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        long[][] rowPref = new long[m][n + 1];
        long[][] colPref = new long[m + 1][n];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                rowPref[r][c + 1] = rowPref[r][c] + grid[r][c];
                colPref[r + 1][c] = colPref[r][c] + grid[r][c];
            }
        }
        for (int k = Math.min(m, n); k >= 2; k--) {
            for (int r = 0; r <= m - k; r++) {
                for (int c = 0; c <= n - k; c++) {
                    long target = rowPref[r][c + k] - rowPref[r][c];
                    boolean ok = true;
                    for (int i = 1; i < k; i++) {
                        if (rowPref[r + i][c + k] - rowPref[r + i][c] != target) {
                            ok = false;
                            break;
                        }
                    }
                    if (!ok) continue;
                    for (int j = 0; j < k; j++) {
                        if (colPref[r + k][c + j] - colPref[r][c + j] != target) {
                            ok = false;
                            break;
                        }
                    }
                    if (!ok) continue;
                    long d1 = 0, d2 = 0;
                    for (int i = 0; i < k; i++) {
                        d1 += grid[r + i][c + i];
                        d2 += grid[r + i][c + k - 1 - i];
                    }
                    if (d1 == target && d2 == target) return k;
                }
            }
        }
        return 1;
    }
}
