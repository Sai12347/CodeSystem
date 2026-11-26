class Solution {
    public int countUnguarded(int m, int n, int[][] guards, int[][] walls) {
        int[][] grid = new int[m][n];
        for (int[] g : guards) grid[g[0]][g[1]] = 1;
        for (int[] w : walls) grid[w[0]][w[1]] = 2;
        int[][] dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        for (int[] g : guards) {
            for (int[] d : dirs) {
                int nr = g[0] + d[0], nc = g[1] + d[1];
                while (nr >= 0 && nr < m && nc >= 0 && nc < n) {
                    int cell = grid[nr][nc];
                    if (cell == 1 || cell == 2) break;
                    grid[nr][nc] = 3;
                    nr += d[0];
                    nc += d[1];
                }
            }
        }
        int ans = 0;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (grid[r][c] == 0) ans++;
            }
        }
        return ans;
    }
}
