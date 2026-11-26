class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        best = s[0]
        for i in range(n):
            for l, r in ((i, i), (i, i + 1)):
                while l >= 0 and r < n and s[l] == s[r]:
                    if r - l + 1 > len(best):
                        best = s[l:r + 1]
                    l -= 1
                    r += 1
        return best
