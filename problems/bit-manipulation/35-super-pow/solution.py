class Solution:
    def superPow(self, a: int, b: List[int]) -> int:
        MOD = 1337
        base = a % MOD
        ans = 1
        for d in b:
            ans = (pow(ans, 10, MOD) * pow(base, d, MOD)) % MOD
        return ans
