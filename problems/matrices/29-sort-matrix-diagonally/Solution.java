class Solution {
    public int[][] diagonalSort(int[][] mat) {
        int m = mat.length, n = mat[0].length;
        int[][] res = new int[m][n];
        for (int r = 0; r < m; r++) res[r] = mat[r].clone();
        int maxLen = Math.min(m, n);
        int[] buf = new int[maxLen];
        for (int sr = 0; sr < m; sr++) {
            int len = 0, r = sr, c = 0;
            while (r < m && c < n) buf[len++] = res[r++][c++];
            Arrays.sort(buf, 0, len);
            r = sr; c = 0;
            for (int i = 0; i < len; i++) res[r++][c++] = buf[i];
        }
        for (int sc = 1; sc < n; sc++) {
            int len = 0, r = 0, c = sc;
            while (r < m && c < n) buf[len++] = res[r++][c++];
            Arrays.sort(buf, 0, len);
            r = 0; c = sc;
            for (int i = 0; i < len; i++) res[r++][c++] = buf[i];
        }
        return res;
    }
}
