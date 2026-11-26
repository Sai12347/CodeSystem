class Solution:
    def removeParentheses(self, s: str) -> str:
        sign_stack = [1]
        local_sign = 1
        out = []
        for ch in s:
            if ch == '+':
                local_sign = 1
            elif ch == '-':
                local_sign = -1
            elif ch == '(':
                sign_stack.append(sign_stack[-1] * local_sign)
                local_sign = 1
            elif ch == ')':
                sign_stack.pop()
            else:
                eff = sign_stack[-1] * local_sign
                if eff == -1:
                    out.append('-')
                elif out:
                    out.append('+')
                out.append(ch)
                local_sign = 1
        return "".join(out)
