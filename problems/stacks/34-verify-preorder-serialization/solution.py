class Solution:
    def isValidSerialization(self, preorder: str) -> bool:
        stack = []
        for tok in preorder.split(","):
            stack.append(tok)
            while len(stack) >= 3 and stack[-1] == "#" and stack[-2] == "#" and stack[-3] != "#":
                stack.pop()
                stack.pop()
                stack[-1] = "#"
        return stack == ["#"]
