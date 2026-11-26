class Solution:
    def modPow(self, base: int, exp: int, mod: int) -> int:
        res = 1 % mod
        b = base % mod
        e = exp
        while e > 0:
            if e & 1:
                res = (res * b) % mod
            b = (b * b) % mod
            e >>= 1
        return res
