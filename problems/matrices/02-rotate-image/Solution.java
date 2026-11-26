class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;
        for (int r = 0; r < n; r++) {
            for (int c = r + 1; c < n; c++) {
                int tmp = matrix[r][c];
                matrix[r][c] = matrix[c][r];
                matrix[c][r] = tmp;
            }
        }
        for (int r = 0; r < n; r++) {
            for (int left = 0, right = n - 1; left < right; left++, right--) {
                int tmp = matrix[r][left];
                matrix[r][left] = matrix[r][right];
                matrix[r][right] = tmp;
            }
        }
    }
}
