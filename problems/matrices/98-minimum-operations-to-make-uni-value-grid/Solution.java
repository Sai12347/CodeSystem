class Solution {
    public int minOperationsUniValue(int[][] grid, int x) {
        int m = grid.length, n = grid[0].length;
        int rem = grid[0][0] % x;
        int[] vals = new int[m * n];
        int idx = 0;
        for (int[] row : grid) {
            for (int v : row) {
                if (v % x != rem) return -1;
                vals[idx++] = v;
            }
        }
        Arrays.sort(vals);
        int med = vals[vals.length / 2];
        int ops = 0;
        for (int v : vals) {
            ops += Math.abs(v - med) / x;
        }
        return ops;
    }
}
