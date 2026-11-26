class Solution:
    def nextHigherSameBits(self, n: int) -> int:
        c = n & -n
        r = n + c
        return (((r ^ n) >> 2) // c) | r
