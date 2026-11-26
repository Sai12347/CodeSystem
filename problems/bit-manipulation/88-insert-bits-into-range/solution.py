class Solution:
    def insertBits(self, n: int, m: int, i: int, j: int) -> int:
        low = (1 << (j - i + 1)) - 1
        field_mask = low << i
        res = (((n & 0xFFFFFFFF) & ~field_mask) | (((m & low) << i))) & 0xFFFFFFFF
        return res - 0x100000000 if res >= 0x80000000 else res
