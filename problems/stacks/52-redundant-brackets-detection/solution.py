class Solution:
    def hasRedundantBrackets(self, s: str) -> bool:
        stack = []
        ops = {'+', '-', '*', '/'}
        for ch in s:
            if ch == ')':
                has_op = False
                while stack and stack[-1] != '(':
                    if stack.pop() in ops:
                        has_op = True
                if stack:
                    stack.pop()
                if not has_op:
                    return True
            else:
                stack.append(ch)
        return False
