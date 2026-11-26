class Solution:
    def evalBooleanInfix(self, expr: str) -> bool:
        prec = {'|': 1, '^': 2, '&': 3, '!': 4}
        vals = []
        ops = []

        def apply_top():
            op = ops.pop()
            if op == '!':
                vals.append(not vals.pop())
            else:
                b = vals.pop()
                a = vals.pop()
                if op == '&':
                    vals.append(a and b)
                elif op == '|':
                    vals.append(a or b)
                else:
                    vals.append(a != b)

        for ch in expr:
            if ch == ' ':
                continue
            if ch == 'T':
                vals.append(True)
            elif ch == 'F':
                vals.append(False)
            elif ch == '(' or ch == '!':
                ops.append(ch)
            elif ch == ')':
                while ops and ops[-1] != '(':
                    apply_top()
                ops.pop()
            else:
                p = prec[ch]
                while ops and ops[-1] != '(' and prec[ops[-1]] >= p:
                    apply_top()
                ops.append(ch)
        while ops:
            apply_top()
        return vals[-1]
