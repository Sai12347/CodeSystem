class Solution {
    public int[][] imageSmoother(int[][] img) {
        int m = img.length, n = img[0].length;
        int[][] res = new int[m][n];
        for (int r = 0; r < m; r++) {
            int r0 = Math.max(0, r - 1), r1 = Math.min(m - 1, r + 1);
            for (int c = 0; c < n; c++) {
                int c0 = Math.max(0, c - 1), c1 = Math.min(n - 1, c + 1);
                int total = 0, cnt = 0;
                for (int nr = r0; nr <= r1; nr++) {
                    for (int nc = c0; nc <= c1; nc++) {
                        total += img[nr][nc];
                        cnt++;
                    }
                }
                res[r][c] = total / cnt;
            }
        }
        return res;
    }
}
