class Solution {
    public int[][] allCellsDistOrder(int rows, int cols, int rCenter, int cCenter) {
        int maxD = Math.max(rCenter, rows - 1 - rCenter) + Math.max(cCenter, cols - 1 - cCenter);
        List<List<int[]>> buckets = new ArrayList<>(maxD + 1);
        for (int d = 0; d <= maxD; d++) buckets.add(new ArrayList<>());
        for (int r = 0; r < rows; r++) {
            int dr = Math.abs(r - rCenter);
            for (int c = 0; c < cols; c++) {
                buckets.get(dr + Math.abs(c - cCenter)).add(new int[]{r, c});
            }
        }
        int[][] res = new int[rows * cols][2];
        int idx = 0;
        for (List<int[]> b : buckets) {
            for (int[] cell : b) {
                res[idx++] = cell;
            }
        }
        return res;
    }
}
