class Solution:
    def minNonZeroProduct(self, p: int) -> int:
        MOD = 1_000_000_007
        max_val = (1 << p) - 1
        pair_base = (max_val - 1) % MOD
        pair_cnt = (1 << (p - 1)) - 1
        return ((max_val % MOD) * pow(pair_base, pair_cnt, MOD)) % MOD
