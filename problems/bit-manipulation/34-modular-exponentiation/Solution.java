class Solution {
    public long modPow(long base, long exp, long mod) {
        long res = 1 % mod;
        long b = base % mod;
        long e = exp;
        while (e > 0) {
            if ((e & 1L) == 1L) {
                res = (res * b) % mod;
            }
            b = (b * b) % mod;
            e >>= 1;
        }
        return res;
    }
}
