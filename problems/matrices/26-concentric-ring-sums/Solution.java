class Solution {
    public int[] concentricRingSums(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        int rings = (Math.min(m, n) + 1) / 2;
        int[] res = new int[rings];
        int top = 0, bottom = m - 1, left = 0, right = n - 1, idx = 0;
        while (top <= bottom && left <= right) {
            int s = 0;
            for (int c = left; c <= right; c++) s += matrix[top][c];
            if (bottom > top) {
                for (int c = left; c <= right; c++) s += matrix[bottom][c];
            }
            for (int r = top + 1; r < bottom; r++) {
                s += matrix[r][left];
                if (right > left) s += matrix[r][right];
            }
            res[idx++] = s;
            top++;
            bottom--;
            left++;
            right--;
        }
        return res;
    }
}
