class Solution {
    public long xorArithmeticArray(long n, long start) {
        long s = start >> 1;
        long high = xorTo(s + n - 1) ^ xorTo(s - 1);
        long low = (start & 1L) & (n & 1L);
        return (high << 1) | low;
    }

    private long xorTo(long x) {
        if (x < 0) return 0L;
        long r = x & 3L;
        if (r == 0L) return x;
        if (r == 1L) return 1L;
        if (r == 2L) return x + 1L;
        return 0L;
    }
}
