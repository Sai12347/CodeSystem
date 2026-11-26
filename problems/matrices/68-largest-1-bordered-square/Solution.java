class Solution {
    public int largest1BorderedSquare(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[][] hor = new int[m][n];
        int[][] ver = new int[m][n];
        int best = 0;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (grid[r][c] == 1) {
                    hor[r][c] = (c > 0 ? hor[r][c - 1] : 0) + 1;
                    ver[r][c] = (r > 0 ? ver[r - 1][c] : 0) + 1;
                    int side = Math.min(hor[r][c], ver[r][c]);
                    while (side > best) {
                        if (hor[r - side + 1][c] >= side && ver[r][c - side + 1] >= side) {
                            best = side;
                            break;
                        }
                        side--;
                    }
                }
            }
        }
        return best * best;
    }
}
