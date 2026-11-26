class Solution {
    public long mortonEncode(int x, int y) {
        return spread(x) | (spread(y) << 1);
    }

    private long spread(long v) {
        v = (v | (v << 8)) & 0x00FF00FFL;
        v = (v | (v << 4)) & 0x0F0F0F0FL;
        v = (v | (v << 2)) & 0x33333333L;
        v = (v | (v << 1)) & 0x55555555L;
        return v;
    }
}
