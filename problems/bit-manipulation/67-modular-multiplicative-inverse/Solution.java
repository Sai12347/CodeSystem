class Solution {
    public long modInverse(long a, long p) {
        long base = a % p;
        if (base == 0L) return -1L;
        long exp = p - 2L;
        long res = 1L;
        while (exp > 0L) {
            if ((exp & 1L) != 0L) {
                res = (res * base) % p;
            }
            base = (base * base) % p;
            exp >>= 1;
        }
        return res;
    }
}
