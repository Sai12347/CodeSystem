class Solution {
    public int[] encodeSignedVarint(int n) {
        long u = Integer.toUnsignedLong((n << 1) ^ (n >> 31));
        int[] buf = new int[5];
        int len = 0;
        while (u >= 0x80L) {
            buf[len++] = (int) ((u & 0x7FL) | 0x80L);
            u >>>= 7;
        }
        buf[len++] = (int) u;
        return Arrays.copyOf(buf, len);
    }
}
