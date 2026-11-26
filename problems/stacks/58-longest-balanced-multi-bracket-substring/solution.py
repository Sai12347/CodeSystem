class Solution:
    def longestMultiBracketSubstring(self, s: str) -> int:
        match = {')': '(', ']': '[', '}': '{'}
        stack = [('#', -1)]
        best = 0
        for i, ch in enumerate(s):
            if ch in '([{':
                stack.append((ch, i))
            elif stack[-1][0] == match[ch]:
                stack.pop()
                span = i - stack[-1][1]
                if span > best:
                    best = span
            else:
                stack.append((ch, i))
        return best
