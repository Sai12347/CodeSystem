class Solution {
    public int[] snakeTraverse(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        int[] res = new int[m * n];
        int idx = 0;
        for (int r = 0; r < m; r++) {
            if ((r & 1) == 0) {
                for (int c = 0; c < n; c++) res[idx++] = matrix[r][c];
            } else {
                for (int c = n - 1; c >= 0; c--) res[idx++] = matrix[r][c];
            }
        }
        return res;
    }
}
