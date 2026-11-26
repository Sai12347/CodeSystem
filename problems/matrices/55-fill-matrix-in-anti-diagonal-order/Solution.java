class Solution {
    public int[][] fillAntiDiagonal(int rows, int cols) {
        int[][] res = new int[rows][cols];
        int val = 1;
        for (int d = 0; d <= rows + cols - 2; d++) {
            int rStart = Math.max(0, d - cols + 1);
            int rEnd = Math.min(rows - 1, d);
            for (int r = rStart; r <= rEnd; r++) {
                res[r][d - r] = val++;
            }
        }
        return res;
    }
}
