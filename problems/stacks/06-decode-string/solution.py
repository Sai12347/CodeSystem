class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        cur = []
        k = 0
        for ch in s:
            if ch.isdigit():
                k = k * 10 + (ord(ch) - 48)
            elif ch == "[":
                stack.append((cur, k))
                cur = []
                k = 0
            elif ch == "]":
                prev, repeat = stack.pop()
                prev.append("".join(cur) * repeat)
                cur = prev
            else:
                cur.append(ch)
        return "".join(cur)
