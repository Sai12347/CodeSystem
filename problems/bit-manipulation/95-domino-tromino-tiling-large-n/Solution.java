class Solution {
    public int numTilingsLargeN(long n) {
        final long MOD = 1_000_000_007L;
        if (n == 1L) return 1;
        if (n == 2L) return 2;
        long[][] res = {
            {1, 0, 0},
            {0, 1, 0},
            {0, 0, 1}
        };
        long[][] base = {
            {2, 0, 1},
            {1, 0, 0},
            {0, 1, 0}
        };
        long exp = n - 2L;
        while (exp > 0L) {
            if ((exp & 1L) != 0L) res = mul(res, base, MOD);
            base = mul(base, base, MOD);
            exp >>= 1;
        }
        long ans = (res[0][0] * 2L + res[0][1] + res[0][2]) % MOD;
        return (int) ans;
    }

    private long[][] mul(long[][] a, long[][] b, long mod) {
        long[][] c = new long[3][3];
        for (int i = 0; i < 3; i++) {
            for (int k = 0; k < 3; k++) {
                long v = a[i][k];
                if (v == 0L) continue;
                for (int j = 0; j < 3; j++) {
                    c[i][j] = (c[i][j] + v * b[k][j]) % mod;
                }
            }
        }
        return c;
    }
}
