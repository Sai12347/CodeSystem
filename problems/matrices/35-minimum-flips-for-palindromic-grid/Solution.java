class Solution {
    public int minFlips(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int rowFlips = 0;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n / 2; c++) {
                if (grid[r][c] != grid[r][n - 1 - c]) rowFlips++;
            }
        }
        int colFlips = 0;
        for (int c = 0; c < n; c++) {
            for (int r = 0; r < m / 2; r++) {
                if (grid[r][c] != grid[m - 1 - r][c]) colFlips++;
            }
        }
        return Math.min(rowFlips, colFlips);
    }
}
