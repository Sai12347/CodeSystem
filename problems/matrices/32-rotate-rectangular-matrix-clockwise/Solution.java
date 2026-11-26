class Solution {
    public int[][] rotateMatrix(int[][] matrix, int rotations) {
        int m = matrix.length, n = matrix[0].length;
        int k = rotations % 4;
        if (k == 0) {
            int[][] res = new int[m][n];
            for (int r = 0; r < m; r++) res[r] = matrix[r].clone();
            return res;
        }
        if (k == 1) {
            int[][] res = new int[n][m];
            for (int r = 0; r < m; r++)
                for (int c = 0; c < n; c++)
                    res[c][m - 1 - r] = matrix[r][c];
            return res;
        }
        if (k == 2) {
            int[][] res = new int[m][n];
            for (int r = 0; r < m; r++)
                for (int c = 0; c < n; c++)
                    res[m - 1 - r][n - 1 - c] = matrix[r][c];
            return res;
        }
        int[][] res = new int[n][m];
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                res[n - 1 - c][r] = matrix[r][c];
        return res;
    }
}
