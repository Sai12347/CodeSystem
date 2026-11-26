class Solution {
    public long nextHigherSameBits(long n) {
        long c = n & -n;
        long r = n + c;
        return (((r ^ n) >> 2) / c) | r;
    }
}
