class Solution {
    public int maxSumSubmatrix(int[][] matrix, int k) {
        int m = matrix.length, n = matrix[0].length;
        int[][] mat = matrix;
        if (m > n) {
            mat = new int[n][m];
            for (int r = 0; r < m; r++)
                for (int c = 0; c < n; c++)
                    mat[c][r] = matrix[r][c];
            int tmp = m; m = n; n = tmp;
        }
        int ans = Integer.MIN_VALUE;
        for (int top = 0; top < m; top++) {
            int[] colSums = new int[n];
            for (int bottom = top; bottom < m; bottom++) {
                int[] row = mat[bottom];
                for (int c = 0; c < n; c++) colSums[c] += row[c];
                int cur = colSums[0], bestK = cur;
                for (int c = 1; c < n; c++) {
                    cur = cur < 0 ? colSums[c] : cur + colSums[c];
                    if (cur > bestK) bestK = cur;
                }
                if (bestK <= k) {
                    if (bestK > ans) ans = bestK;
                    if (ans == k) return k;
                    continue;
                }
                TreeSet<Integer> set = new TreeSet<>();
                set.add(0);
                int pref = 0;
                for (int x : colSums) {
                    pref += x;
                    Integer ceil = set.ceiling(pref - k);
                    if (ceil != null) {
                        int cand = pref - ceil;
                        if (cand > ans) {
                            ans = cand;
                            if (ans == k) return k;
                        }
                    }
                    set.add(pref);
                }
            }
        }
        return ans;
    }
}
