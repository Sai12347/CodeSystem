class Solution:
    def minEnd(self, n: int, x: int) -> int:
        res = x
        rem = n - 1
        bit = 1
        while rem > 0:
            if (res & bit) == 0:
                if rem & 1:
                    res |= bit
                rem >>= 1
            bit <<= 1
        return res
