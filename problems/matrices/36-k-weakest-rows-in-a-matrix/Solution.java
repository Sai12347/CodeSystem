class Solution {
    public int[] kWeakestRows(int[][] mat, int k) {
        int m = mat.length, n = mat[0].length;
        int[][] pairs = new int[m][2];
        for (int r = 0; r < m; r++) {
            int lo = 0, hi = n;
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (mat[r][mid] == 1) lo = mid + 1;
                else hi = mid;
            }
            pairs[r][0] = lo;
            pairs[r][1] = r;
        }
        Arrays.sort(pairs, (a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        int[] res = new int[k];
        for (int i = 0; i < k; i++) res[i] = pairs[i][1];
        return res;
    }
}
