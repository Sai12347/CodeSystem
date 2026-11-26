class Solution:
    def evaluateLisp(self, expression: str) -> int:
        n = len(expression)
        idx = 0
        scopes = []

        def lookup(var: str) -> int:
            for sc in reversed(scopes):
                if var in sc:
                    return sc[var]
            return 0

        def read_token() -> str:
            nonlocal idx
            start = idx
            while idx < n and expression[idx] not in (' ', ')'):
                idx += 1
            return expression[start:idx]

        def eval_atom(tok: str) -> int:
            if tok[0] == '-' or tok[0].isdigit():
                return int(tok)
            return lookup(tok)

        def eval_expr() -> int:
            nonlocal idx
            if expression[idx] != '(':
                return eval_atom(read_token())
            idx += 1  # skip '('
            op = read_token()
            idx += 1  # skip ' '
            if op == 'add':
                a = eval_expr()
                idx += 1  # skip ' '
                b = eval_expr()
                idx += 1  # skip ')'
                return a + b
            if op == 'mult':
                a = eval_expr()
                idx += 1
                b = eval_expr()
                idx += 1
                return a * b
            # let
            scopes.append({})
            while True:
                if expression[idx] == '(':
                    res = eval_expr()
                    idx += 1  # skip ')'
                    scopes.pop()
                    return res
                tok = read_token()
                if expression[idx] == ')':
                    res = eval_atom(tok)
                    idx += 1  # skip ')'
                    scopes.pop()
                    return res
                idx += 1  # skip ' '
                val = eval_expr()
                scopes[-1][tok] = val
                idx += 1  # skip ' '

        return eval_expr()
