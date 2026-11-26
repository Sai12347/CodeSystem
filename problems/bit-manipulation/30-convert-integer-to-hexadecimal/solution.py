class Solution:
    def toHex(self, num: int) -> str:
        if num == 0:
            return "0"
        digits = "0123456789abcdef"
        n = num & 0xFFFFFFFF
        out = []
        while n > 0:
            out.append(digits[n & 0xF])
            n >>= 4
        return "".join(reversed(out))
