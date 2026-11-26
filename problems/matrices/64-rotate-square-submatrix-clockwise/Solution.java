class Solution {
    public int[][] rotateSubmatrix(int[][] grid, int row, int col, int k, int turns) {
        int m = grid.length, n = grid[0].length;
        int[][] res = new int[m][n];
        for (int r = 0; r < m; r++) res[r] = grid[r].clone();
        int t = turns % 4;
        if (t == 0 || k == 1) return res;
        for (int dr = 0; dr < k; dr++) {
            for (int dc = 0; dc < k; dc++) {
                int val = grid[row + dr][col + dc];
                if (t == 1) {
                    res[row + dc][col + k - 1 - dr] = val;
                } else if (t == 2) {
                    res[row + k - 1 - dr][col + k - 1 - dc] = val;
                } else {
                    res[row + k - 1 - dc][col + dr] = val;
                }
            }
        }
        return res;
    }
}
