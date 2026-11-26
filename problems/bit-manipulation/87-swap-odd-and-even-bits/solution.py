class Solution:
    def swapOddEvenBits(self, n: int) -> int:
        u = n & 0xFFFFFFFF
        res = (((u & 0xAAAAAAAA) >> 1) | ((u & 0x55555555) << 1)) & 0xFFFFFFFF
        return res - 0x100000000 if res >= 0x80000000 else res
