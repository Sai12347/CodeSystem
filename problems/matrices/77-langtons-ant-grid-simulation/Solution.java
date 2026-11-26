class Solution {
    public int[][] simulateLangtonsAnt(int[][] grid, int startRow, int startCol, int steps) {
        int m = grid.length, n = grid[0].length;
        int[][] res = new int[m][n];
        for (int i = 0; i < m; i++) res[i] = grid[i].clone();
        int[] dr = {-1, 0, 1, 0};
        int[] dc = {0, 1, 0, -1};
        int r = startRow, c = startCol, d = 0;
        for (int s = 0; s < steps; s++) {
            if (res[r][c] == 0) {
                d = (d + 1) % 4;
                res[r][c] = 1;
            } else {
                d = (d + 3) % 4;
                res[r][c] = 0;
            }
            r += dr[d];
            c += dc[d];
            if (r < 0 || r >= m || c < 0 || c >= n) break;
        }
        return res;
    }
}
