class Solution:
    def longestNiceSubstring(self, s: str) -> str:
        def solve(l: int, r: int) -> tuple[int, int]:
            if r - l < 2:
                return (0, 0)
            lower = upper = 0
            for i in range(l, r):
                c = ord(s[i])
                if c >= 97:
                    lower |= 1 << (c - 97)
                else:
                    upper |= 1 << (c - 65)
            good = lower & upper
            start = l
            best = (0, 0)
            has_bad = False
            for i in range(l, r):
                c = ord(s[i])
                bit = 1 << (c - 97 if c >= 97 else c - 65)
                if not (good & bit):
                    has_bad = True
                    cand = solve(start, i)
                    if cand[1] - cand[0] > best[1] - best[0]:
                        best = cand
                    start = i + 1
            if not has_bad:
                return (l, r)
            cand = solve(start, r)
            if cand[1] - cand[0] > best[1] - best[0]:
                best = cand
            return best
        a, b = solve(0, len(s))
        return s[a:b]
