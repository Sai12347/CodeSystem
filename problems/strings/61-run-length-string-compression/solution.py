class Solution:
    def compressString(self, s: str) -> str:
        out = []
        n = len(s)
        i = 0
        while i < n:
            j = i + 1
            while j < n and s[j] == s[i]:
                j += 1
            out.append(s[i])
            if j - i > 1:
                out.append(str(j - i))
            i = j
        return "".join(out)
