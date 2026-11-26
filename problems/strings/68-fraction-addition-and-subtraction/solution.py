class Solution:
    def fractionAddition(self, expression: str) -> str:
        num, den = 0, 1
        i, n = 0, len(expression)
        while i < n:
            sign = 1
            if expression[i] in "+-":
                sign = -1 if expression[i] == "-" else 1
                i += 1
            a = 0
            while i < n and expression[i].isdigit():
                a = a * 10 + (ord(expression[i]) - 48)
                i += 1
            i += 1  # skip '/'
            b = 0
            while i < n and expression[i].isdigit():
                b = b * 10 + (ord(expression[i]) - 48)
                i += 1
            num = num * b + sign * a * den
            den *= b
            g = math.gcd(abs(num), den)
            num //= g
            den //= g
        return f"{num}/{den}" 
