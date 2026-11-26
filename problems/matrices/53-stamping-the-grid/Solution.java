class Solution {
    public boolean possibleToStamp(int[][] grid, int stampHeight, int stampWidth) {
        int m = grid.length, n = grid[0].length;
        int h = stampHeight, w = stampWidth;
        int[][] pref = new int[m + 1][n + 1];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                pref[r + 1][c + 1] = grid[r][c] + pref[r][c + 1] + pref[r + 1][c] - pref[r][c];
            }
        }
        int[][] diff = new int[m + 2][n + 2];
        if (h <= m && w <= n) {
            for (int r = 0; r <= m - h; r++) {
                int r2 = r + h;
                for (int c = 0; c <= n - w; c++) {
                    int c2 = c + w;
                    int sum = pref[r2][c2] - pref[r][c2] - pref[r2][c] + pref[r][c];
                    if (sum == 0) {
                        diff[r + 1][c + 1] += 1;
                        diff[r2 + 1][c + 1] -= 1;
                        diff[r + 1][c2 + 1] -= 1;
                        diff[r2 + 1][c2 + 1] += 1;
                    }
                }
            }
        }
        for (int r = 1; r <= m; r++) {
            for (int c = 1; c <= n; c++) {
                diff[r][c] += diff[r - 1][c] + diff[r][c - 1] - diff[r - 1][c - 1];
                if (grid[r - 1][c - 1] == 0 && diff[r][c] == 0) return false;
            }
        }
        return true;
    }
}
