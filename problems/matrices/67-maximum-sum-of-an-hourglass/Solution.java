class Solution {
    public int maxHourglassSum(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int best = Integer.MIN_VALUE;
        for (int r = 0; r < m - 2; r++) {
            for (int c = 0; c < n - 2; c++) {
                int s = grid[r][c] + grid[r][c + 1] + grid[r][c + 2]
                        + grid[r + 1][c + 1]
                        + grid[r + 2][c] + grid[r + 2][c + 1] + grid[r + 2][c + 2];
                if (s > best) best = s;
            }
        }
        return best;
    }
}
