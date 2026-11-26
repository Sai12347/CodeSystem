class Solution {
    public int[] spiralWalkWithObstacles(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[][] dirs = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
        boolean[][] vis = new boolean[m][n];
        int r = 0, c = 0, d = 0;
        vis[0][0] = true;
        List<Integer> list = new ArrayList<>();
        list.add(grid[0][0]);
        while (true) {
            boolean moved = false;
            for (int k = 0; k < 4; k++) {
                int nd = (d + k) % 4;
                int nr = r + dirs[nd][0];
                int nc = c + dirs[nd][1];
                if (nr >= 0 && nr < m && nc >= 0 && nc < n && !vis[nr][nc] && grid[nr][nc] != -1) {
                    r = nr;
                    c = nc;
                    d = nd;
                    vis[r][c] = true;
                    list.add(grid[r][c]);
                    moved = true;
                    break;
                }
            }
            if (!moved) break;
        }
        int[] ans = new int[list.size()];
        for (int i = 0; i < list.size(); i++) ans[i] = list.get(i);
        return ans;
    }
}
