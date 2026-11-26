class Solution {
    public int insertBits(int n, int m, int i, int j) {
        long low = (1L << (j - i + 1)) - 1L;
        long fieldMask = low << i;
        long res = ((n & 0xFFFFFFFFL) & ~fieldMask) | (((m & low) << i));
        return (int) res;
    }
}
