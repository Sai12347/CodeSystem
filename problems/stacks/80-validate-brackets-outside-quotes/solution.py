class Solution:
    def isValidOutsideQuotes(self, s: str) -> bool:
        match = {')': '(', ']': '[', '}': '{'}
        stack = []
        in_quote = False
        escaped = False
        for ch in s:
            if in_quote:
                if escaped:
                    escaped = False
                elif ch == '\\':
                    escaped = True
                elif ch == '"':
                    in_quote = False
            else:
                if ch == '"':
                    in_quote = True
                elif ch in '([{':
                    stack.append(ch)
                elif ch in match:
                    if not stack or stack[-1] != match[ch]:
                        return False
                    stack.pop()
        return (not in_quote) and (not stack)
