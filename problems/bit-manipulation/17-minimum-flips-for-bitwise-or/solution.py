class Solution:
    def minFlipsForOr(self, a: int, b: int, c: int) -> int:
        diff = (a | b) ^ c
        return diff.bit_count() + (a & b & diff).bit_count()
