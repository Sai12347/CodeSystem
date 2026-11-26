class Solution:
    def isValid(self, s: str) -> bool:
        if len(s) % 3 != 0:
            return False
        stack = []
        for ch in s:
            if ch == "c":
                if len(stack) < 2 or stack[-1] != "b" or stack[-2] != "a":
                    return False
                stack.pop()
                stack.pop()
            else:
                stack.append(ch)
        return not stack
