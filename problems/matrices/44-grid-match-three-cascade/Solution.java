class Solution {
    public int[][] candyCrush(int[][] board) {
        int m = board.length, n = board[0].length;
        int[][] g = new int[m][n];
        for (int r = 0; r < m; r++) g[r] = board[r].clone();
        while (true) {
            boolean[][] crush = new boolean[m][n];
            boolean changed = false;
            for (int r = 0; r < m; r++) {
                for (int c = 0; c < n - 2; c++) {
                    int v = g[r][c];
                    if (v != 0 && v == g[r][c + 1] && v == g[r][c + 2]) {
                        crush[r][c] = crush[r][c + 1] = crush[r][c + 2] = true;
                        changed = true;
                    }
                }
            }
            for (int c = 0; c < n; c++) {
                for (int r = 0; r < m - 2; r++) {
                    int v = g[r][c];
                    if (v != 0 && v == g[r + 1][c] && v == g[r + 2][c]) {
                        crush[r][c] = crush[r + 1][c] = crush[r + 2][c] = true;
                        changed = true;
                    }
                }
            }
            if (!changed) return g;
            for (int c = 0; c < n; c++) {
                int write = m - 1;
                for (int r = m - 1; r >= 0; r--) {
                    if (!crush[r][c] && g[r][c] != 0) {
                        g[write--][c] = g[r][c];
                    }
                }
                while (write >= 0) g[write--][c] = 0;
            }
        }
    }
}
