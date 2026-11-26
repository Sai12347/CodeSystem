class Solution {
    public boolean isPrimeLarge(long n) {
        if (n < 2L) return false;
        long[] small = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
        for (long p : small) {
            if (n == p) return true;
            if (n % p == 0L) return false;
        }
        long d = n - 1L;
        int s = 0;
        while ((d & 1L) == 0L) {
            d >>= 1;
            s++;
        }
        for (long a : small) {
            long x = powMod(a % n, d, n);
            if (x == 1L || x == n - 1L) continue;
            boolean witness = true;
            for (int r = 1; r < s; r++) {
                x = mulMod(x, x, n);
                if (x == n - 1L) {
                    witness = false;
                    break;
                }
            }
            if (witness) return false;
        }
        return true;
    }

    private long mulMod(long a, long b, long mod) {
        long res = 0L;
        long x = a % mod;
        long y = b % mod;
        while (y > 0L) {
            if ((y & 1L) != 0L) {
                res += x;
                if (res >= mod) res -= mod;
            }
            x += x;
            if (x >= mod) x -= mod;
            y >>= 1;
        }
        return res;
    }

    private long powMod(long base, long exp, long mod) {
        long res = 1L;
        long b = base % mod;
        long e = exp;
        while (e > 0L) {
            if ((e & 1L) != 0L) res = mulMod(res, b, mod);
            b = mulMod(b, b, mod);
            e >>= 1;
        }
        return res;
    }
}
