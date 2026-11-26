class Solution:
    def countGoodDigitStrings(self, n: int) -> int:
        MOD = 1_000_000_007
        even_cnt = (n + 1) // 2
        odd_cnt = n // 2
        return (pow(5, even_cnt, MOD) * pow(4, odd_cnt, MOD)) % MOD
