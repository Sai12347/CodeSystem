class Solution {
    public long maxQuadrantSum(int[][] matrix) {
        int m = matrix.length;
        int n = m / 2;
        long total = 0;
        for (int r = 0; r < n; r++) {
            int mr = m - 1 - r;
            for (int c = 0; c < n; c++) {
                int mc = m - 1 - c;
                int best = Math.max(
                    Math.max(matrix[r][c], matrix[r][mc]),
                    Math.max(matrix[mr][c], matrix[mr][mc])
                );
                total += best;
            }
        }
        return total;
    }
}
