class Solution:
    def longestBalancedPrefix(self, s: str) -> int:
        match = {')': '(', ']': '[', '}': '{'}
        stack = []
        best = 0
        for i, ch in enumerate(s):
            if ch in '([{':
                stack.append(ch)
            else:
                if not stack or stack[-1] != match[ch]:
                    break
                stack.pop()
                if not stack:
                    best = i + 1
        return best
