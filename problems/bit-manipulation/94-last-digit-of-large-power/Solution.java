class Solution {
    public int lastDigitOfPower(long base, long exp) {
        int res = 1;
        int b = (int) (base % 10L);
        long e = exp;
        while (e > 0L) {
            if ((e & 1L) != 0L) {
                res = (res * b) % 10;
            }
            b = (b * b) % 10;
            e >>= 1;
        }
        return res;
    }
}
