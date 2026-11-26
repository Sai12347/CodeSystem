class Solution:
    def waysToFillArray(self, queries: List[List[int]]) -> List[int]:
        MOD = 1_000_000_007
        max_n = max(q[0] for q in queries)
        max_k = max(q[1] for q in queries)
        limit = max_n + 15

        fact = [1] * (limit + 1)
        for i in range(1, limit + 1):
            fact[i] = (fact[i - 1] * i) % MOD
        inv_fact = [1] * (limit + 1)
        inv_fact[limit] = pow(fact[limit], MOD - 2, MOD)
        for i in range(limit, 0, -1):
            inv_fact[i - 1] = (inv_fact[i] * i) % MOD

        spf = list(range(max_k + 1))
        p = 2
        while p * p <= max_k:
            if spf[p] == p:
                for m in range(p * p, max_k + 1, p):
                    if spf[m] == m:
                        spf[m] = p
            p += 1

        ans = []
        for n, k in queries:
            ways = 1
            x = k
            while x > 1:
                prime = spf[x]
                exp = 0
                while x % prime == 0:
                    x //= prime
                    exp += 1
                comb = fact[n + exp - 1] * inv_fact[exp] % MOD * inv_fact[n - 1] % MOD
                ways = (ways * comb) % MOD
            ans.append(ways)
        return ans
