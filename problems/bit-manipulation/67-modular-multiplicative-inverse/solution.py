class Solution:
    def modInverse(self, a: int, p: int) -> int:
        base = a % p
        if base == 0:
            return -1
        exp = p - 2
        res = 1
        while exp > 0:
            if exp & 1:
                res = (res * base) % p
            base = (base * base) % p
            exp >>= 1
        return res
