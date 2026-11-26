class Solution:
    def evalSetExpression(self, expr: str) -> List[int]:
        prec = {'|': 1, '-': 1, '^': 1, '&': 2}
        vals = []
        ops = []

        def apply_top():
            op = ops.pop()
            b = vals.pop()
            a = vals.pop()
            if op == '&':
                vals.append(a & b)
            elif op == '|':
                vals.append(a | b)
            elif op == '-':
                vals.append(a - b)
            else:
                vals.append(a ^ b)

        i = 0
        n = len(expr)
        while i < n:
            ch = expr[i]
            if ch == ' ':
                i += 1
            elif ch == '{':
                j = expr.index('}', i)
                inner = expr[i + 1:j].strip()
                s = set()
                if inner:
                    for part in inner.split(','):
                        s.add(int(part.strip()))
                vals.append(s)
                i = j + 1
            elif ch == '(':
                ops.append(ch)
                i += 1
            elif ch == ')':
                while ops and ops[-1] != '(':
                    apply_top()
                ops.pop()
                i += 1
            else:
                p = prec[ch]
                while ops and ops[-1] != '(' and prec[ops[-1]] >= p:
                    apply_top()
                ops.append(ch)
                i += 1
        while ops:
            apply_top()
        return sorted(vals[-1])
