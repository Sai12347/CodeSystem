class Solution:
    def toBalancedTernary(self, n: int) -> str:
        if n == 0:
            return "0"
        digits = []
        x = n
        while x != 0:
            r = x % 3
            if r == 0:
                digits.append("0")
                x //= 3
            elif r == 1:
                digits.append("+")
                x = (x - 1) // 3
            else:
                digits.append("-")
                x = (x + 1) // 3
        digits.reverse()
        return "".join(digits)
