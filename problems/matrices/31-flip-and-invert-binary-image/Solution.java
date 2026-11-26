class Solution {
    public int[][] flipAndInvertImage(int[][] image) {
        int n = image.length;
        int[][] res = new int[n][n];
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                res[r][c] = 1 - image[r][n - 1 - c];
            }
        }
        return res;
    }
}
