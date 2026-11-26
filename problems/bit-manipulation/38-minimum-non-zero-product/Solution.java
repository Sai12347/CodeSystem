class Solution {
    public int minNonZeroProduct(int p) {
        final long MOD = 1_000_000_007L;
        long maxVal = (1L << p) - 1L;
        long pairBase = (maxVal - 1L) % MOD;
        long pairCnt = (1L << (p - 1)) - 1L;
        long res = 1L;
        long b = pairBase;
        long e = pairCnt;
        while (e > 0) {
            if ((e & 1L) == 1L) res = (res * b) % MOD;
            b = (b * b) % MOD;
            e >>= 1;
        }
        return (int) (((maxVal % MOD) * res) % MOD);
    }
}
