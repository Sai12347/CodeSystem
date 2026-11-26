class Solution {
    public int numSubmat(int[][] mat) {
        int m = mat.length, n = mat[0].length;
        int[] heights = new int[n];
        int[] stack = new int[n];
        int[] rowSum = new int[n];
        int total = 0;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                heights[c] = mat[r][c] == 1 ? heights[c] + 1 : 0;
            }
            int top = -1;
            for (int c = 0; c < n; c++) {
                while (top >= 0 && heights[stack[top]] >= heights[c]) top--;
                if (top >= 0) {
                    int prev = stack[top];
                    rowSum[c] = rowSum[prev] + heights[c] * (c - prev);
                } else {
                    rowSum[c] = heights[c] * (c + 1);
                }
                stack[++top] = c;
                total += rowSum[c];
            }
        }
        return total;
    }
}
