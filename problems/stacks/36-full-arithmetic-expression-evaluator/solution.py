class Solution:
    def evaluateExpression(self, s: str) -> int:
        def apply_op(terms, op, val):
            if op == '+':
                terms.append(val)
            elif op == '-':
                terms.append(-val)
            elif op == '*':
                terms[-1] *= val
            else:
                terms[-1] = int(terms[-1] / val)

        frames = []
        terms = []
        op = '+'
        num = 0
        for ch in s:
            if ch == ' ':
                continue
            if ch.isdigit():
                num = num * 10 + (ord(ch) - 48)
            elif ch == '(':
                frames.append((terms, op))
                terms = []
                op = '+'
                num = 0
            elif ch == ')':
                apply_op(terms, op, num)
                val = sum(terms)
                terms, op = frames.pop()
                num = val
            else:
                apply_op(terms, op, num)
                op = ch
                num = 0
        apply_op(terms, op, num)
        return sum(terms)
