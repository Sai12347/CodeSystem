class Solution:
    def evaluateMinMax(self, expr: str) -> int:
        ops = []
        vals = []
        i = 0
        n = len(expr)
        while i < n:
            ch = expr[i]
            if ch == 'm':
                ops.append('n' if expr[i + 1] == 'i' else 'x')
                i += 4
            elif ch == ',':
                i += 1
            elif ch == ')':
                b = vals.pop()
                a = vals.pop()
                op = ops.pop()
                vals.append(a if (a < b if op == 'n' else a > b) else b)
                i += 1
            else:
                sign = 1
                if ch == '-':
                    sign = -1
                    i += 1
                num = 0
                while i < n and expr[i].isdigit():
                    num = num * 10 + (ord(expr[i]) - 48)
                    i += 1
                vals.append(sign * num)
        return vals[0]
