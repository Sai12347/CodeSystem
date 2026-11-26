class Solution {
    public int maxNiceDivisors(int primeFactors) {
        final long MOD = 1_000_000_007L;
        if (primeFactors <= 3) return primeFactors;
        long q = primeFactors / 3;
        int r = primeFactors % 3;
        if (r == 0) return (int) modPow(3L, q, MOD);
        if (r == 1) return (int) ((modPow(3L, q - 1L, MOD) * 4L) % MOD);
        return (int) ((modPow(3L, q, MOD) * 2L) % MOD);
    }

    private long modPow(long base, long exp, long mod) {
        long res = 1L;
        long b = base % mod;
        long e = exp;
        while (e > 0L) {
            if ((e & 1L) != 0L) res = (res * b) % mod;
            b = (b * b) % mod;
            e >>= 1;
        }
        return res;
    }
}
