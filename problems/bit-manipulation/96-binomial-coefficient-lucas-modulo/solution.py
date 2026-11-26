class Solution:
    def binomialModPrime(self, n: int, k: int, p: int) -> int:
        fact = [1] * p
        for i in range(1, p):
            fact[i] = (fact[i - 1] * i) % p
        inv_fact = [1] * p
        inv_fact[p - 1] = pow(fact[p - 1], p - 2, p)
        for i in range(p - 2, 0, -1):
            inv_fact[i] = (inv_fact[i + 1] * (i + 1)) % p

        ans = 1
        nn, kk = n, k
        while nn > 0 or kk > 0:
            ni = nn % p
            ki = kk % p
            if ki > ni:
                return 0
            ans = (ans * fact[ni] % p * inv_fact[ki] % p * inv_fact[ni - ki]) % p
            nn //= p
            kk //= p
        return ans
