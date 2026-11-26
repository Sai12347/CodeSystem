class Solution:
    def robotWithString(self, s: str) -> str:
        n = len(s)
        suf_min = ['{'] * (n + 1)
        for i in range(n - 1, -1, -1):
            suf_min[i] = s[i] if s[i] < suf_min[i + 1] else suf_min[i + 1]
        stack = []
        out = []
        for i, ch in enumerate(s):
            stack.append(ch)
            nxt = suf_min[i + 1]
            while stack and stack[-1] <= nxt:
                out.append(stack.pop())
        return "".join(out)
