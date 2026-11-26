class Solution {
    public int matrixMedian(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        long lo = grid[0][0], hi = grid[0][n - 1];
        for (int r = 1; r < m; r++) {
            if (grid[r][0] < lo) lo = grid[r][0];
            if (grid[r][n - 1] > hi) hi = grid[r][n - 1];
        }
        int need = (m * n + 1) / 2;
        while (lo < hi) {
            long mid = lo + (hi - lo) / 2;
            int cnt = 0;
            for (int[] row : grid) {
                int l = 0, r = n;
                while (l < r) {
                    int k = (l + r) >>> 1;
                    if (row[k] <= mid) l = k + 1;
                    else r = k;
                }
                cnt += l;
            }
            if (cnt >= need) hi = mid;
            else lo = mid + 1;
        }
        return (int) lo;
    }
}
