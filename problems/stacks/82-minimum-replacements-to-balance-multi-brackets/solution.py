class Solution:
    def minBracketReplacements(self, s: str) -> int:
        match = {')': '(', ']': '[', '}': '{', '>': '<'}
        stack = []
        reps = 0
        for ch in s:
            if ch in '([{<':
                stack.append(ch)
            else:
                if not stack:
                    return -1
                if stack.pop() != match[ch]:
                    reps += 1
        return reps if not stack else -1
