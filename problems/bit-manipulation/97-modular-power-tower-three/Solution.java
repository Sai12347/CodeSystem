class Solution {
    public long modPowerTower(long a, long b, long c, long p) {
        if (b == 0L && c > 0L) return 1L;
        long aMod = a % p;
        if (aMod == 0L) return 0L;
        if (p == 2L) return 1L;
        long e = modPow(b % (p - 1L), c, p - 1L);
        return modPow(aMod, e, p);
    }

    private long modPow(long base, long exp, long mod) {
        long res = 1L % mod;
        long b = base % mod;
        long e = exp;
        while (e > 0L) {
            if ((e & 1L) != 0L) res = (res * b) % mod;
            b = (b * b) % mod;
            e >>= 1;
        }
        return res;
    }
}
