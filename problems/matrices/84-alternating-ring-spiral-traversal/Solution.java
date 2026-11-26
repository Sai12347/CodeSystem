class Solution {
    public int[] alternatingRingSpiral(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        int[] res = new int[m * n];
        int idx = 0;
        int top = 0, bottom = m - 1, left = 0, right = n - 1;
        int layer = 0;
        while (top <= bottom && left <= right) {
            if (layer % 2 == 0) {
                for (int c = left; c <= right; c++) res[idx++] = matrix[top][c];
                for (int r = top + 1; r <= bottom; r++) res[idx++] = matrix[r][right];
                if (top < bottom) {
                    for (int c = right - 1; c >= left; c--) res[idx++] = matrix[bottom][c];
                }
                if (left < right) {
                    for (int r = bottom - 1; r > top; r--) res[idx++] = matrix[r][left];
                }
            } else {
                for (int r = top; r <= bottom; r++) res[idx++] = matrix[r][left];
                if (left < right) {
                    for (int c = left + 1; c <= right; c++) res[idx++] = matrix[bottom][c];
                }
                if (top < bottom && left < right) {
                    for (int r = bottom - 1; r >= top; r--) res[idx++] = matrix[r][right];
                    for (int c = right - 1; c > left; c--) res[idx++] = matrix[top][c];
                }
            }
            top++;
            bottom--;
            left++;
            right--;
            layer++;
        }
        return res;
    }
}
