class Solution {
    public void solve(char[][] board) {
        if (board == null || board.length == 0 || board[0].length == 0) {
            return;
        }
        int rows = board.length;
        int cols = board[0].length;
        int[] qr = new int[rows * cols];
        int[] qc = new int[rows * cols];
        int head = 0, tail = 0;

        for (int r = 0; r < rows; r++) {
            if (board[r][0] == 'O') {
                board[r][0] = 'S';
                qr[tail] = r;
                qc[tail++] = 0;
            }
            if (board[r][cols - 1] == 'O') {
                board[r][cols - 1] = 'S';
                qr[tail] = r;
                qc[tail++] = cols - 1;
            }
        }
        for (int c = 0; c < cols; c++) {
            if (board[0][c] == 'O') {
                board[0][c] = 'S';
                qr[tail] = 0;
                qc[tail++] = c;
            }
            if (board[rows - 1][c] == 'O') {
                board[rows - 1][c] = 'S';
                qr[tail] = rows - 1;
                qc[tail++] = c;
            }
        }

        while (head < tail) {
            int r = qr[head];
            int c = qc[head++];
            if (r > 0 && board[r - 1][c] == 'O') {
                board[r - 1][c] = 'S';
                qr[tail] = r - 1;
                qc[tail++] = c;
            }
            if (r + 1 < rows && board[r + 1][c] == 'O') {
                board[r + 1][c] = 'S';
                qr[tail] = r + 1;
                qc[tail++] = c;
            }
            if (c > 0 && board[r][c - 1] == 'O') {
                board[r][c - 1] = 'S';
                qr[tail] = r;
                qc[tail++] = c - 1;
            }
            if (c + 1 < cols && board[r][c + 1] == 'O') {
                board[r][c + 1] = 'S';
                qr[tail] = r;
                qc[tail++] = c + 1;
            }
        }

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (board[r][c] == 'O') {
                    board[r][c] = 'X';
                } else if (board[r][c] == 'S') {
                    board[r][c] = 'O';
                }
            }
        }
    }
}
