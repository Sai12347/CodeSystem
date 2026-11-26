class Solution {
    public int countSubmatrices(int[][] grid, int k) {
        int n = grid[0].length;
        long[] colSum = new long[n];
        int ans = 0;
        for (int[] row : grid) {
            long cur = 0;
            for (int c = 0; c < n; c++) {
                colSum[c] += row[c];
                cur += colSum[c];
                if (cur <= k) {
                    ans++;
                } else {
                    break;
                }
            }
        }
        return ans;
    }
}
