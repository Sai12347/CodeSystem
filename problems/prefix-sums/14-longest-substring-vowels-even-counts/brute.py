class Solution:
    def findTheLongestSubstring(self, s: str) -> int:
        vowel_bit = {"a": 1, "e": 2, "i": 4, "o": 8, "u": 16}
        n = len(s)
        best = 0
        for i in range(n):
            mask = 0
            for j in range(i, n):
                bit = vowel_bit.get(s[j])
                if bit:
                    mask ^= bit
                if mask == 0 and (j - i + 1) > best:
                    best = j - i + 1
        return best
