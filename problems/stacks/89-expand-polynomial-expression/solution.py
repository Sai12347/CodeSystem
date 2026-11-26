class Solution:
    def expandPolynomial(self, expr: str) -> List[int]:
        def trim(p):
            while len(p) > 1 and p[-1] == 0:
                p.pop()
            return p

        def apply_op(vals, ops):
            op = ops.pop()
            b = vals.pop()
            a = vals.pop()
            if op == '+' or op == '-':
                sign = 1 if op == '+' else -1
                m = max(len(a), len(b))
                res = [0] * m
                for k in range(m):
                    va = a[k] if k < len(a) else 0
                    vb = b[k] if k < len(b) else 0
                    res[k] = va + sign * vb
                vals.append(trim(res))
            else:
                res = [0] * (len(a) + len(b) - 1)
                for i, va in enumerate(a):
                    if va == 0:
                        continue
                    for j, vb in enumerate(b):
                        res[i + j] += va * vb
                vals.append(trim(res))

        prec = {'+': 1, '-': 1, '*': 2}
        vals = []
        ops = []
        i = 0
        n = len(expr)
        while i < n:
            ch = expr[i]
            if ch == ' ':
                i += 1
            elif ch == 'x':
                vals.append([0, 1])
                i += 1
            elif '0' <= ch <= '9':
                num = 0
                while i < n and '0' <= expr[i] <= '9':
                    num = num * 10 + (ord(expr[i]) - 48)
                    i += 1
                vals.append([num])
            elif ch == '(':
                ops.append(ch)
                i += 1
            elif ch == ')':
                while ops and ops[-1] != '(':
                    apply_op(vals, ops)
                ops.pop()
                i += 1
            else:
                p = prec[ch]
                while ops and ops[-1] != '(' and prec[ops[-1]] >= p:
                    apply_op(vals, ops)
                ops.append(ch)
                i += 1
        while ops:
            apply_op(vals, ops)
        return vals[-1]
