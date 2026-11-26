class Solution:
    def evalWithPower(self, s: str) -> int:
        def prec(op: str) -> int:
            if op in ('+', '-'):
                return 1
            if op == '*':
                return 2
            if op == '^':
                return 3
            return 0

        vals = []
        ops = []

        def apply_top() -> None:
            op = ops.pop()
            b = vals.pop()
            a = vals.pop()
            if op == '+':
                vals.append(a + b)
            elif op == '-':
                vals.append(a - b)
            elif op == '*':
                vals.append(a * b)
            else:
                res = 1
                base = a
                exp = b
                while exp > 0:
                    if exp & 1:
                        res *= base
                    base *= base
                    exp >>= 1
                vals.append(res)

        i = 0
        n = len(s)
        while i < n:
            ch = s[i]
            if ch == ' ':
                i += 1
            elif ch.isdigit():
                num = 0
                while i < n and s[i].isdigit():
                    num = num * 10 + (ord(s[i]) - 48)
                    i += 1
                vals.append(num)
            elif ch == '(':
                ops.append(ch)
                i += 1
            elif ch == ')':
                while ops and ops[-1] != '(':
                    apply_top()
                ops.pop()
                i += 1
            else:
                p = prec(ch)
                while ops and ops[-1] != '(' and (prec(ops[-1]) > p or (ch != '^' and prec(ops[-1]) == p)):
                    apply_top()
                ops.append(ch)
                i += 1
        while ops:
            apply_top()
        return vals[-1]
