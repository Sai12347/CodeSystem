class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        stack = []
        rem = k
        for ch in num:
            while rem > 0 and stack and stack[-1] > ch:
                stack.pop()
                rem -= 1
            stack.append(ch)
        if rem > 0:
            stack = stack[:-rem]
        res = "".join(stack).lstrip("0")
        return res if res else "0"

