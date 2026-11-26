class Solution {
    public boolean exist(char[][] board, String word) {
        int m = board.length;
        int n = board[0].length;
        int len = word.length();
        if (len > m * n) return false;

        int[] boardCnt = new int[128];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                boardCnt[board[r][c]]++;
            }
        }
        int[] wordCnt = new int[128];
        for (int i = 0; i < len; i++) {
            char ch = word.charAt(i);
            if (++wordCnt[ch] > boardCnt[ch]) return false;
        }

        char[] chars = word.toCharArray();
        if (boardCnt[chars[0]] > boardCnt[chars[len - 1]]) {
            for (int l = 0, r = len - 1; l < r; l++, r--) {
                char tmp = chars[l];
                chars[l] = chars[r];
                chars[r] = tmp;
            }
        }

        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (board[r][c] == chars[0] && dfs(board, chars, r, c, 0, m, n)) {
                    return true;
                }
            }
        }
        return false;
    }

    private boolean dfs(char[][] board, char[] word, int r, int c, int idx, int m, int n) {
        if (board[r][c] != word[idx]) return false;
        if (idx == word.length - 1) return true;
        char saved = board[r][c];
        board[r][c] = '#';
        int nxt = idx + 1;
        boolean found = (r > 0 && dfs(board, word, r - 1, c, nxt, m, n))
                || (r + 1 < m && dfs(board, word, r + 1, c, nxt, m, n))
                || (c > 0 && dfs(board, word, r, c - 1, nxt, m, n))
                || (c + 1 < n && dfs(board, word, r, c + 1, nxt, m, n));
        board[r][c] = saved;
        return found;
    }
}
