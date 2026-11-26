class Solution {
    public int[] waysToFillArray(int[][] queries) {
        final long MOD = 1_000_000_007L;
        int maxN = 1, maxK = 1;
        for (int[] q : queries) {
            if (q[0] > maxN) maxN = q[0];
            if (q[1] > maxK) maxK = q[1];
        }
        int limit = maxN + 15;
        long[] fact = new long[limit + 1];
        fact[0] = 1;
        for (int i = 1; i <= limit; i++) {
            fact[i] = (fact[i - 1] * i) % MOD;
        }
        long[] invFact = new long[limit + 1];
        invFact[limit] = modPow(fact[limit], MOD - 2, MOD);
        for (int i = limit; i >= 1; i--) {
            invFact[i - 1] = (invFact[i] * i) % MOD;
        }

        int[] spf = new int[maxK + 1];
        for (int i = 0; i <= maxK; i++) spf[i] = i;
        for (int p = 2; p * p <= maxK; p++) {
            if (spf[p] == p) {
                for (int m = p * p; m <= maxK; m += p) {
                    if (spf[m] == m) spf[m] = p;
                }
            }
        }

        int[] ans = new int[queries.length];
        for (int i = 0; i < queries.length; i++) {
            int n = queries[i][0], x = queries[i][1];
            long ways = 1;
            while (x > 1) {
                int prime = spf[x];
                int exp = 0;
                while (x % prime == 0) {
                    x /= prime;
                    exp++;
                }
                long comb = fact[n + exp - 1] * invFact[exp] % MOD * invFact[n - 1] % MOD;
                ways = (ways * comb) % MOD;
            }
            ans[i] = (int) ways;
        }
        return ans;
    }

    private long modPow(long base, long exp, long mod) {
        long res = 1;
        long b = base % mod;
        long e = exp;
        while (e > 0) {
            if ((e & 1L) == 1L) res = (res * b) % mod;
            b = (b * b) % mod;
            e >>= 1;
        }
        return res;
    }
}
