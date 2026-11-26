class Solution:
    def minReversals(self, s: str) -> int:
        if len(s) % 2 == 1:
            return -1
        stack = []
        for ch in s:
            if ch == ')' and stack and stack[-1] == '(':
                stack.pop()
            else:
                stack.append(ch)
        opens = sum(1 for ch in stack if ch == '(')
        closes = len(stack) - opens
        return (opens + 1) // 2 + (closes + 1) // 2
