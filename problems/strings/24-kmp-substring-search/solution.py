class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if not needle: return 0
        lps = [0] * len(needle)
        j = 0
        for i in range(1, len(needle)):
            while j and needle[i] != needle[j]: j = lps[j - 1]
            if needle[i] == needle[j]: j += 1; lps[i] = j
        j = 0
        for i, c in enumerate(haystack):
            while j and c != needle[j]: j = lps[j - 1]
            if c == needle[j]: j += 1
            if j == len(needle): return i - j + 1
        return -1
