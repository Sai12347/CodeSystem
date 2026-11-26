class Solution {
    public void solveSudoku(char[][] board) {
        int[] rows = new int[9];
        int[] cols = new int[9];
        int[] boxes = new int[9];
        int[] emptyR = new int[81];
        int[] emptyC = new int[81];
        int emptyCount = 0;

        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                char ch = board[r][c];
                if (ch == '.') {
                    emptyR[emptyCount] = r;
                    emptyC[emptyCount] = c;
                    emptyCount++;
                } else {
                    int bit = 1 << (ch - '1');
                    rows[r] |= bit;
                    cols[c] |= bit;
                    boxes[(r / 3) * 3 + (c / 3)] |= bit;
                }
            }
        }

        dfs(0, emptyCount, emptyR, emptyC, board, rows, cols, boxes);
    }

    private boolean dfs(int idx, int n, int[] emptyR, int[] emptyC,
                        char[][] board, int[] rows, int[] cols, int[] boxes) {
        if (idx == n) return true;

        int best = idx;
        int bestCnt = 10;
        int bestMask = 0;
        for (int i = idx; i < n; i++) {
            int r = emptyR[i];
            int c = emptyC[i];
            int bi = (r / 3) * 3 + (c / 3);
            int avail = 0x1FF & ~(rows[r] | cols[c] | boxes[bi]);
            int cnt = Integer.bitCount(avail);
            if (cnt == 0) return false;
            if (cnt < bestCnt) {
                bestCnt = cnt;
                best = i;
                bestMask = avail;
                if (cnt == 1) break;
            }
        }

        int tr = emptyR[idx]; emptyR[idx] = emptyR[best]; emptyR[best] = tr;
        int tc = emptyC[idx]; emptyC[idx] = emptyC[best]; emptyC[best] = tc;

        int r = emptyR[idx];
        int c = emptyC[idx];
        int bi = (r / 3) * 3 + (c / 3);
        int m = bestMask;
        while (m != 0) {
            int bit = m & -m;
            m ^= bit;
            int d = Integer.numberOfTrailingZeros(bit);
            board[r][c] = (char) ('1' + d);
            rows[r] |= bit;
            cols[c] |= bit;
            boxes[bi] |= bit;
            if (dfs(idx + 1, n, emptyR, emptyC, board, rows, cols, boxes)) {
                return true;
            }
            rows[r] ^= bit;
            cols[c] ^= bit;
            boxes[bi] ^= bit;
            board[r][c] = '.';
        }

        tr = emptyR[idx]; emptyR[idx] = emptyR[best]; emptyR[best] = tr;
        tc = emptyC[idx]; emptyC[idx] = emptyC[best]; emptyC[best] = tc;
        return false;
    }
}
