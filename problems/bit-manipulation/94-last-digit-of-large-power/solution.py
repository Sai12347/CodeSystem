class Solution:
    def lastDigitOfPower(self, base: int, exp: int) -> int:
        res = 1
        b = base % 10
        e = exp
        while e > 0:
            if e & 1:
                res = (res * b) % 10
            b = (b * b) % 10
            e >>= 1
        return res
