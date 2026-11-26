class Solution {
    public int numRookCaptures(char[][] board) {
        int m = board.length, n = board[0].length;
        int rr = 0, rc = 0;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (board[r][c] == 'R') {
                    rr = r;
                    rc = c;
                }
            }
        }
        int[][] dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        int captures = 0;
        for (int[] d : dirs) {
            int r = rr + d[0], c = rc + d[1];
            while (r >= 0 && r < m && c >= 0 && c < n) {
                char ch = board[r][c];
                if (ch == 'B') break;
                if (ch == 'p') {
                    captures++;
                    break;
                }
                r += d[0];
                c += d[1];
            }
        }
        return captures;
    }
}
