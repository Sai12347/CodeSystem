class Solution:
    def decodeString(self, s: str) -> str:
        while "[" in s:
            r = s.index("]")
            l = s.rindex("[", 0, r)
            d = l - 1
            while d >= 0 and s[d].isdigit():
                d -= 1
            k = int(s[d + 1 : l])
            s = s[: d + 1] + s[l + 1 : r] * k + s[r + 1 :]
        return s
