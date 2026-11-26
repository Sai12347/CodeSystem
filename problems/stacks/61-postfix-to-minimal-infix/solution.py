class Solution:
    def postfixToInfix(self, expr: str) -> str:
        prec_map = {'+': 1, '-': 1, '*': 2}
        stack = []
        for tok in expr.split():
            if tok in prec_map:
                p = prec_map[tok]
                r_str, r_p = stack.pop()
                l_str, l_p = stack.pop()
                if l_p < p:
                    l_str = f"({l_str})"
                if r_p < p or (r_p == p and tok == '-'):
                    r_str = f"({r_str})"
                stack.append((f"{l_str}{tok}{r_str}", p))
            else:
                stack.append((tok, 3))
        return stack[-1][0]
