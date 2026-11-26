class Solution {
    public int binomialModPrime(long n, long k, int p) {
        long[] fact = new long[p];
        fact[0] = 1L;
        for (int i = 1; i < p; i++) {
            fact[i] = (fact[i - 1] * i) % p;
        }
        long[] invFact = new long[p];
        invFact[p - 1] = modPow(fact[p - 1], p - 2, p);
        for (int i = p - 2; i >= 0; i--) {
            invFact[i] = (invFact[i + 1] * (i + 1)) % p;
        }
        long ans = 1L;
        long nn = n, kk = k;
        while (nn > 0L || kk > 0L) {
            int ni = (int) (nn % p);
            int ki = (int) (kk % p);
            if (ki > ni) return 0;
            ans = ans * fact[ni] % p * invFact[ki] % p * invFact[ni - ki] % p;
            nn /= p;
            kk /= p;
        }
        return (int) ans;
    }

    private long modPow(long base, long exp, long mod) {
        long res = 1L;
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
