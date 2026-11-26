class Solution:
    def myPow(self, x: float, n: int) -> float:
        exp = n
        base = x
        if exp < 0:
            base = 1.0 / base
            exp = -exp
        res = 1.0
        while exp > 0:
            if exp & 1:
                res *= base
            base *= base
            exp >>= 1
        return res
