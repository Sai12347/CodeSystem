class Solution:
    def infixToPrefix(self, s: str) -> str:
        prec = {'+': 1, '-': 1, '*': 2, '/': 2}
        ops = []
        out = []
        for ch in reversed(s):
            if ch == ' ':
                continue
            if 'a' <= ch <= 'z':
                out.append(ch)
            elif ch == ')':
                ops.append(ch)
            elif ch == '(':
                while ops and ops[-1] != ')':
                    out.append(ops.pop())
                ops.pop()
            else:
                p = prec[ch]
                while ops and ops[-1] != ')' and prec[ops[-1]] > p:
                    out.append(ops.pop())
                ops.append(ch)
        while ops:
            out.append(ops.pop())
        out.reverse()
        return "".join(out)
