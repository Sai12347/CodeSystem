class Solution:
    def modPowerTower(self, a: int, b: int, c: int, p: int) -> int:
        if b == 0 and c > 0:
            return 1
        a_mod = a % p
        if a_mod == 0:
            return 0
        if p == 2:
            return 1
        e = pow(b % (p - 1), c, p - 1)
        return pow(a_mod, e, p)
