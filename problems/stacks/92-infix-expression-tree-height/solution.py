class Solution:
    def expressionTreeHeight(self, s: str) -> int:
        prec = {'+': 1, '-': 1, '*': 2, '/': 2}
        heights = []
        ops = []

        def apply_top():
            ops.pop()
            hr = heights.pop()
            hl = heights.pop()
            heights.append(1 + (hl if hl > hr else hr))

        i = 0
        n = len(s)
        while i < n:
            ch = s[i]
            if ch == ' ':
                i += 1
            elif '0' <= ch <= '9':
                while i < n and '0' <= s[i] <= '9':
                    i += 1
                heights.append(0)
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
        return heights[-1]
