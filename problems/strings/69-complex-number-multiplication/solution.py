class Solution:
    def complexNumberMultiply(self, num1: str, num2: str) -> str:
        p1 = num1.index('+')
        p2 = num2.index('+')
        a, b = int(num1[:p1]), int(num1[p1 + 1:-1])
        c, d = int(num2[:p2]), int(num2[p2 + 1:-1])
        return f"{a * c - b * d}+{a * d + b * c}i" 
