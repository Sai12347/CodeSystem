class Solution {
    public int countGoodDigitStrings(long n) {
        final long MOD = 1_000_000_007L;
        long evenCnt = (n + 1) / 2;
        long oddCnt = n / 2;
        return (int) ((modPow(5L, evenCnt, MOD) * modPow(4L, oddCnt, MOD)) % MOD);
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
