class Solution:
    def geometricSeriesMod(self, a: int, n: int, mod: int) -> int:
        ans = 0
        cur_sum = 1 % mod
        cur_pow = a % mod
        rem = n
        while rem > 0:
            if rem & 1:
                ans = (ans * cur_pow + cur_sum) % mod
            cur_sum = (cur_sum * (1 + cur_pow)) % mod
            cur_pow = (cur_pow * cur_pow) % mod
            rem >>= 1
        return ans
