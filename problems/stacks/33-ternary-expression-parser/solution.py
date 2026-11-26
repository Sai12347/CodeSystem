class Solution:
    def parseTernary(self, expression: str) -> str:
        stack = []
        for i in range(len(expression) - 1, -1, -1):
            ch = expression[i]
            if stack and stack[-1] == '?':
                stack.pop()
                t_val = stack.pop()
                f_val = stack.pop()
                stack.append(t_val if ch == 'T' else f_val)
            elif ch != ':':
                stack.append(ch)
        return stack[-1]
