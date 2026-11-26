class Solution {
    public int countWalks(int n, int[][] edges, int src, int dst, long k) {
        final long MOD = 1_000_000_007L;
        long[][] base = new long[n][n];
        for (int[] e : edges) {
            base[e[0]][e[1]]++;
        }
        long[][] res = new long[n][n];
        for (int i = 0; i < n; i++) res[i][i] = 1L;

        long exp = k;
        while (exp > 0L) {
            if ((exp & 1L) != 0L) res = mul(res, base, n, MOD);
            base = mul(base, base, n, MOD);
            exp >>= 1;
        }
        return (int) res[src][dst];
    }

    private long[][] mul(long[][] a, long[][] b, int n, long mod) {
        long[][] c = new long[n][n];
        for (int i = 0; i < n; i++) {
            for (int mid = 0; mid < n; mid++) {
                long v = a[i][mid];
                if (v == 0L) continue;
                for (int j = 0; j < n; j++) {
                    c[i][j] = (c[i][j] + v * b[mid][j]) % mod;
                }
            }
        }
        return c;
    }
}
