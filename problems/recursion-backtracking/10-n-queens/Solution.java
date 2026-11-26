class Solution {
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> res = new ArrayList<>();
        int[] queens = new int[n];
        String[] rowStrs = new String[n];
        for (int c = 0; c < n; c++) {
            char[] arr = new char[n];
            Arrays.fill(arr, '.');
            arr[c] = 'Q';
            rowStrs[c] = new String(arr);
        }
        int full = (1 << n) - 1;
        backtrack(0, n, full, 0, 0, 0, queens, rowStrs, res);
        return res;
    }

    private void backtrack(int row, int n, int full, int cols, int d1, int d2,
                           int[] queens, String[] rowStrs, List<List<String>> res) {
        if (row == n) {
            List<String> board = new ArrayList<>(n);
            for (int r = 0; r < n; r++) {
                board.add(rowStrs[queens[r]]);
            }
            res.add(board);
            return;
        }
        int avail = full & ~(cols | d1 | d2);
        while (avail != 0) {
            int bit = avail & -avail;
            avail ^= bit;
            queens[row] = Integer.numberOfTrailingZeros(bit);
            backtrack(row + 1, n, full, cols | bit, (d1 | bit) << 1, (d2 | bit) >> 1, queens, rowStrs, res);
        }
    }
}
