class Solution:
    def isValid(self, s: str) -> bool:
        if len(s) % 2 == 1:
            return False
        match = {")": "(", "]": "[", "}": "{"}
        stack = []
        for ch in s:
            if ch in match:
                if not stack or stack.pop() != match[ch]:
                    return False
            else:
                stack.append(ch)
        return not stack
