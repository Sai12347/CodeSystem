class Solution {
    public int[][] restoreMatrix(int[] rowSum, int[] colSum) {
        int m = rowSum.length, n = colSum.length;
        int[] rRem = Arrays.copyOf(rowSum, m);
        int[] cRem = Arrays.copyOf(colSum, n);
        int[][] ans = new int[m][n];
        int r = 0, c = 0;
        while (r < m && c < n) {
            int val = Math.min(rRem[r], cRem[c]);
            ans[r][c] = val;
            rRem[r] -= val;
            cRem[c] -= val;
            if (rRem[r] == 0) r++;
            if (cRem[c] == 0) c++;
        }
        return ans;
    }
}
