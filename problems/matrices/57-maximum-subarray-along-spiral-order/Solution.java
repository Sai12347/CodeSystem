class Solution {
    public int maxSpiralSubarraySum(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        int top = 0, bottom = m - 1, left = 0, right = n - 1;
        boolean started = false;
        int cur = 0, best = Integer.MIN_VALUE;
        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) {
                int v = matrix[top][c];
                cur = started ? Math.max(v, cur + v) : v;
                started = true;
                if (cur > best) best = cur;
            }
            top++;
            for (int r = top; r <= bottom; r++) {
                int v = matrix[r][right];
                cur = started ? Math.max(v, cur + v) : v;
                started = true;
                if (cur > best) best = cur;
            }
            right--;
            if (top <= bottom) {
                for (int c = right; c >= left; c--) {
                    int v = matrix[bottom][c];
                    cur = started ? Math.max(v, cur + v) : v;
                    started = true;
                    if (cur > best) best = cur;
                }
                bottom--;
            }
            if (left <= right) {
                for (int r = bottom; r >= top; r--) {
                    int v = matrix[r][left];
                    cur = started ? Math.max(v, cur + v) : v;
                    started = true;
                    if (cur > best) best = cur;
                }
                left++;
            }
        }
        return best;
    }
}
