class Solution {
    public long minOpsRotationalSymmetry(int[][] grid) {
        int n = grid.length;
        long ops = 0;
        int[] vals = new int[4];
        for (int r = 0; r < n / 2; r++) {
            for (int c = 0; c < (n + 1) / 2; c++) {
                vals[0] = grid[r][c];
                vals[1] = grid[c][n - 1 - r];
                vals[2] = grid[n - 1 - r][n - 1 - c];
                vals[3] = grid[n - 1 - c][r];
                Arrays.sort(vals);
                ops += ((long) vals[3] - vals[0]) + ((long) vals[2] - vals[1]);
            }
        }
        return ops;
    }
}
