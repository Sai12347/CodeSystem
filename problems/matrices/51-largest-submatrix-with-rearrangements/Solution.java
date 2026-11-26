class Solution {
    public int largestSubmatrix(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        int[] heights = new int[n];
        int[] sorted = new int[n];
        int ans = 0;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                heights[c] = matrix[r][c] == 1 ? heights[c] + 1 : 0;
                sorted[c] = heights[c];
            }
            Arrays.sort(sorted);
            for (int i = n - 1; i >= 0; i--) {
                int h = sorted[i];
                if (h == 0) break;
                int area = h * (n - i);
                if (area > ans) ans = area;
            }
        }
        return ans;
    }
}
