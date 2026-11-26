class Solution {
    public boolean hasRotationalSymmetry(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        for (int r = 0; r < (m + 1) / 2; r++) {
            int mr = m - 1 - r;
            int colLimit = (r == mr) ? (n + 1) / 2 : n;
            for (int c = 0; c < colLimit; c++) {
                if (grid[r][c] != grid[mr][n - 1 - c]) return false;
            }
        }
        return true;
    }
}
