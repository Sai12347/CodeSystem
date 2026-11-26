class Solution:
    def xorArithmeticArray(self, n: int, start: int) -> int:
        def xor_to(x: int) -> int:
            if x < 0:
                return 0
            r = x & 3
            if r == 0:
                return x
            if r == 1:
                return 1
            if r == 2:
                return x + 1
            return 0

        s = start >> 1
        high = xor_to(s + n - 1) ^ xor_to(s - 1)
        low = (start & 1) & (n & 1)
        return (high << 1) | low
