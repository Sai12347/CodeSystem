class Solution:
    def evalPrefix(self, tokens: List[str]) -> int:
        stack = []
        for tok in reversed(tokens):
            if tok in ('+', '-', '*', '/'):
                a = stack.pop()
                b = stack.pop()
                if tok == '+':
                    stack.append(a + b)
                elif tok == '-':
                    stack.append(a - b)
                elif tok == '*':
                    stack.append(a * b)
                else:
                    stack.append(int(a / b))
            else:
                stack.append(int(tok))
        return stack[-1]
