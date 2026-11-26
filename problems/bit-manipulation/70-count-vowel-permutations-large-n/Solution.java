class Solution {
    public int countVowelPermutation(long n) {
        final long MOD = 1_000_000_007L;
        long[][] res = new long[5][5];
        for (int i = 0; i < 5; i++) res[i][i] = 1L;
        long[][] base = {
            {0, 1, 1, 0, 1},
            {1, 0, 1, 0, 0},
            {0, 1, 0, 1, 0},
            {0, 0, 1, 0, 0},
            {0, 0, 1, 1, 0}
        };
        long exp = n - 1L;
        while (exp > 0L) {
            if ((exp & 1L) != 0L) res = mul(res, base, MOD);
            base = mul(base, base, MOD);
            exp >>= 1;
        }
        long total = 0L;
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                total = (total + res[i][j]) % MOD;
            }
        }
        return (int) total;
    }

    private long[][] mul(long[][] a, long[][] b, long mod) {
        long[][] c = new long[5][5];
        for (int i = 0; i < 5; i++) {
            for (int k = 0; k < 5; k++) {
                long v = a[i][k];
                if (v == 0L) continue;
                for (int j = 0; j < 5; j++) {
                    c[i][j] = (c[i][j] + v * b[k][j]) % mod;
                }
            }
        }
        return c;
    }
}
