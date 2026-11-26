class Solution {
    public int fibonacciMod(long n) {
        return (int) fib(n)[0];
    }

    private long[] fib(long k) {
        final long MOD = 1_000_000_007L;
        if (k == 0) return new long[]{0L, 1L};
        long[] p = fib(k >> 1);
        long a = p[0], b = p[1];
        long twoBMinusA = ((2 * b - a) % MOD + MOD) % MOD;
        long c = (a * twoBMinusA) % MOD;
        long d = (a * a + b * b) % MOD;
        if ((k & 1L) == 1L) {
            return new long[]{d, (c + d) % MOD};
        }
        return new long[]{c, d};
    }
}
