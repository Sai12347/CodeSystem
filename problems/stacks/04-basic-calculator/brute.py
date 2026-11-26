import sys


class Solution:
    def calculate(self, s: str) -> int:
        sys.setrecursionlimit(10000)
        n = len(s)
        idx = 0

        def skip_ws():
            nonlocal idx
            while idx < n and s[idx] == " ":
                idx += 1

        def parse_expr():
            nonlocal idx
            val = parse_term()
            while True:
                skip_ws()
                if idx < n and s[idx] in "+-":
                    op = s[idx]
                    idx += 1
                    rhs = parse_term()
                    val = val + rhs if op == "+" else val - rhs
                else:
                    break
            return val

        def parse_term():
            nonlocal idx
            skip_ws()
            if s[idx] == "-":
                idx += 1
                return -parse_term()
            if s[idx] == "(":
                idx += 1
                val = parse_expr()
                skip_ws()
                idx += 1  # consume ')'
                return val
            num = 0
            while idx < n and s[idx].isdigit():
                num = num * 10 + (ord(s[idx]) - 48)
                idx += 1
            return num

        return parse_expr()
