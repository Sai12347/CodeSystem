class Solution:
    def infixToPostfix(self, tokens: List[str]) -> List[str]:
        prec = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
        out = []
        ops = []
        for tok in tokens:
            if tok == "(":
                ops.append(tok)
            elif tok == ")":
                while ops and ops[-1] != "(":
                    out.append(ops.pop())
                ops.pop()
            elif tok in prec:
                p = prec[tok]
                while ops and ops[-1] in prec:
                    tp = prec[ops[-1]]
                    if tp > p or (tp == p and tok != "^"):
                        out.append(ops.pop())
                    else:
                        break
                ops.append(tok)
            else:
                out.append(tok)
        while ops:
            out.append(ops.pop())
        return out
