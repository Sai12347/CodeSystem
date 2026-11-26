class Solution {
    public void gameOfLife(int[][] board) {
        int m = board.length, n = board[0].length;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                int live = 0;
                for (int dr = -1; dr <= 1; dr++) {
                    for (int dc = -1; dc <= 1; dc++) {
                        if (dr == 0 && dc == 0) continue;
                        int nr = r + dr, nc = c + dc;
                        if (nr >= 0 && nr < m && nc >= 0 && nc < n && (board[nr][nc] & 1) == 1) {
                            live++;
                        }
                    }
                }
                if ((board[r][c] & 1) == 1) {
                    if (live == 2 || live == 3) board[r][c] |= 2;
                } else if (live == 3) {
                    board[r][c] |= 2;
                }
            }
        }
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                board[r][c] >>= 1;
            }
        }
    }
}
