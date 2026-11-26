class Solution {
    public int[] zOrderTraversal(int[][] grid) {
        int n = grid.length;
        int[] res = new int[n * n];
        int[] idx = new int[1];
        dfs(grid, 0, 0, n, res, idx);
        return res;
    }

    private void dfs(int[][] grid, int r, int c, int size, int[] res, int[] idx) {
        if (size == 1) {
            res[idx[0]++] = grid[r][c];
            return;
        }
        int h = size / 2;
        dfs(grid, r, c, h, res, idx);
        dfs(grid, r, c + h, h, res, idx);
        dfs(grid, r + h, c, h, res, idx);
        dfs(grid, r + h, c + h, h, res, idx);
    }
}
