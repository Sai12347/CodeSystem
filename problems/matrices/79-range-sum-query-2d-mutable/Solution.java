class NumMatrix2D {
    private final int m, n;
    private final int[][] vals;
    private final int[][] bit;

    public NumMatrix2D(int[][] matrix) {
        this.m = matrix.length;
        this.n = matrix[0].length;
        this.vals = new int[m][n];
        this.bit = new int[m + 1][n + 1];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                update(r, c, matrix[r][c]);
            }
        }
    }

    public void update(int row, int col, int val) {
        int delta = val - vals[row][col];
        vals[row][col] = val;
        for (int i = row + 1; i <= m; i += i & -i) {
            for (int j = col + 1; j <= n; j += j & -j) {
                bit[i][j] += delta;
            }
        }
    }

    private int prefix(int r, int c) {
        int total = 0;
        for (int i = r; i > 0; i -= i & -i) {
            for (int j = c; j > 0; j -= j & -j) {
                total += bit[i][j];
            }
        }
        return total;
    }

    public int sumRegion(int row1, int col1, int row2, int col2) {
        return prefix(row2 + 1, col2 + 1)
                - prefix(row1, col2 + 1)
                - prefix(row2 + 1, col1)
                + prefix(row1, col1);
    }
}
