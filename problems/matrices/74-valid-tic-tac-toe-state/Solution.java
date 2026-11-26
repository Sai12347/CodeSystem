class Solution {
    public boolean validTicTacToe(String[] board) {
        int xCnt = 0, oCnt = 0;
        for (int r = 0; r < 3; r++) {
            for (int c = 0; c < 3; c++) {
                char ch = board[r].charAt(c);
                if (ch == 'X') xCnt++;
                else if (ch == 'O') oCnt++;
            }
        }
        if (xCnt != oCnt && xCnt != oCnt + 1) return false;
        boolean xWin = wins(board, 'X');
        boolean oWin = wins(board, 'O');
        if (xWin && oWin) return false;
        if (xWin && xCnt != oCnt + 1) return false;
        if (oWin && xCnt != oCnt) return false;
        return true;
    }

    private boolean wins(String[] b, char ch) {
        for (int i = 0; i < 3; i++) {
            if (b[i].charAt(0) == ch && b[i].charAt(1) == ch && b[i].charAt(2) == ch) return true;
            if (b[0].charAt(i) == ch && b[1].charAt(i) == ch && b[2].charAt(i) == ch) return true;
        }
        if (b[0].charAt(0) == ch && b[1].charAt(1) == ch && b[2].charAt(2) == ch) return true;
        if (b[0].charAt(2) == ch && b[1].charAt(1) == ch && b[2].charAt(0) == ch) return true;
        return false;
    }
}
