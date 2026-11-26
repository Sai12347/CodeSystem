class Solution {
    public int matrixScore(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int score = m * (1 << (n - 1));
        for (int c = 1; c < n; c++) {
            int same = 0;
            for (int r = 0; r < m; r++) {
                if (grid[r][c] == grid[r][0]) same++;
            }
            score += Math.max(same, m - same) * (1 << (n - 1 - c));
        }
        return score;
    }
}
