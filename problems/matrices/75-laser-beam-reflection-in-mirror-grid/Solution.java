class Solution {
    public int illuminatedCells(char[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[] dr = {0, 1, 0, -1};
        int[] dc = {1, 0, -1, 0};
        int[][] seen = new int[m][n];
        int r = 0, c = 0, d = 0, lit = 0;
        while (r >= 0 && r < m && c >= 0 && c < n) {
            int bit = 1 << d;
            if ((seen[r][c] & bit) != 0) break;
            if (seen[r][c] == 0) lit++;
            seen[r][c] |= bit;
            char ch = grid[r][c];
            if (ch == '/') d = 3 - d;
            else if (ch == '\\') d ^= 1;
            r += dr[d];
            c += dc[d];
        }
        return lit;
    }
}
