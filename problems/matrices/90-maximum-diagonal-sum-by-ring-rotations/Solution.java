class Solution {
    public long maxDiagonalSumAfterRingRotations(int[][] matrix) {
        int n = matrix.length;
        long ans = (n % 2 == 1) ? matrix[n / 2][n / 2] : 0L;
        for (int k = 0; k < n / 2; k++) {
            int s = n - 1 - 2 * k;
            long best = Long.MIN_VALUE;
            for (int i = 0; i < s; i++) {
                long cur = (long) matrix[k][k + i]
                    + matrix[k + i][k + s]
                    + matrix[k + s][k + s - i]
                    + matrix[k + s - i][k];
                if (cur > best) best = cur;
            }
            ans += best;
        }
        return ans;
    }
}
