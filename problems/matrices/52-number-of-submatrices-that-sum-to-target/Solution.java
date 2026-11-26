class Solution {
    public int numSubmatrixSumTarget(int[][] matrix, int target) {
        int m = matrix.length, n = matrix[0].length;
        int[][] mat = matrix;
        if (m > n) {
            mat = new int[n][m];
            for (int r = 0; r < m; r++)
                for (int c = 0; c < n; c++)
                    mat[c][r] = matrix[r][c];
            int tmp = m; m = n; n = tmp;
        }
        int ans = 0;
        for (int top = 0; top < m; top++) {
            int[] colSums = new int[n];
            for (int bottom = top; bottom < m; bottom++) {
                int[] row = mat[bottom];
                Map<Integer, Integer> freq = new HashMap<>(n * 2);
                freq.put(0, 1);
                int pref = 0;
                for (int c = 0; c < n; c++) {
                    colSums[c] += row[c];
                    pref += colSums[c];
                    ans += freq.getOrDefault(pref - target, 0);
                    freq.put(pref, freq.getOrDefault(pref, 0) + 1);
                }
            }
        }
        return ans;
    }
}
