class Solution {
    public int[][] rotateGrid(int[][] grid, int k) {
        int m = grid.length, n = grid[0].length;
        int[][] res = new int[m][n];
        int layers = Math.min(m, n) / 2;
        for (int layer = 0; layer < layers; layer++) {
            int top = layer, bottom = m - 1 - layer;
            int left = layer, right = n - 1 - layer;
            int len = 2 * ((bottom - top) + (right - left));
            int[] rs = new int[len];
            int[] cs = new int[len];
            int idx = 0;
            for (int c = left; c < right; c++) { rs[idx] = top; cs[idx++] = c; }
            for (int r = top; r < bottom; r++) { rs[idx] = r; cs[idx++] = right; }
            for (int c = right; c > left; c--) { rs[idx] = bottom; cs[idx++] = c; }
            for (int r = bottom; r > top; r--) { rs[idx] = r; cs[idx++] = left; }
            int shift = k % len;
            for (int i = 0; i < len; i++) {
                int src = (i + shift) % len;
                res[rs[i]][cs[i]] = grid[rs[src]][cs[src]];
            }
        }
        return res;
    }
}
