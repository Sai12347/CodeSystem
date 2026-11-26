class Solution {
    public boolean checkValidKnightTour(int[][] grid) {
        int n = grid.length;
        if (grid[0][0] != 0) return false;
        int[][] moves = {{-2, -1}, {-2, 1}, {-1, -2}, {-1, 2}, {1, -2}, {1, 2}, {2, -1}, {2, 1}};
        int r = 0, c = 0;
        for (int step = 1; step < n * n; step++) {
            boolean found = false;
            for (int[] mv : moves) {
                int nr = r + mv[0], nc = c + mv[1];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] == step) {
                    r = nr;
                    c = nc;
                    found = true;
                    break;
                }
            }
            if (!found) return false;
        }
        return true;
    }
}
