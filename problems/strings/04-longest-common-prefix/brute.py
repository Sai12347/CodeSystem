class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        ordered = sorted(strs)
        a, b = ordered[0], ordered[-1]
        i = 0
        while i < len(a) and i < len(b) and a[i] == b[i]:
            i += 1
        return a[:i]
