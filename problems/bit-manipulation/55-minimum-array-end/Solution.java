class Solution {
    public long minEnd(int n, int x) {
        long res = x;
        long rem = n - 1L;
        long bit = 1L;
        while (rem > 0L) {
            if ((res & bit) == 0L) {
                if ((rem & 1L) != 0L) {
                    res |= bit;
                }
                rem >>= 1;
            }
            bit <<= 1;
        }
        return res;
    }
}
