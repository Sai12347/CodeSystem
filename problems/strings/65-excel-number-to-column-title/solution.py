class Solution:
    def convertToTitle(self, columnNumber: int) -> str:
        out = []
        n = columnNumber
        while n > 0:
            n -= 1
            out.append(chr(65 + n % 26))
            n //= 26
        return "".join(reversed(out))
