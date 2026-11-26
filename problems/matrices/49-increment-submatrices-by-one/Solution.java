class Solution {
    public int[][] rangeAddQueries(int n, int[][] queries) {
        int[][] diff = new int[n + 1][n + 1];
        for (int[] q : queries) {
            int r1 = q[0], c1 = q[1], r2 = q[2], c2 = q[3];
            diff[r1][c1] += 1;
            diff[r1][c2 + 1] -= 1;
            diff[r2 + 1][c1] -= 1;
            diff[r2 + 1][c2 + 1] += 1;
        }
        int[][] res = new int[n][n];
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                int v = diff[r][c];
                if (r > 0) v += res[r - 1][c];
                if (c > 0) v += res[r][c - 1];
                if (r > 0 && c > 0) v -= res[r - 1][c - 1];
                res[r][c] = v;
            }
        }
        return res;
    }
}
