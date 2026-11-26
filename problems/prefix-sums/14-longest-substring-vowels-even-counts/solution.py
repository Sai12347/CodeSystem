class Solution:
    def findTheLongestSubstring(self, s: str) -> int:
        vowel_bit = {"a": 1, "e": 2, "i": 4, "o": 8, "u": 16}
        first = [-2] * 32
        first[0] = -1
        mask = 0
        best = 0
        for i, ch in enumerate(s):
            bit = vowel_bit.get(ch)
            if bit:
                mask ^= bit
            if first[mask] != -2:
                length = i - first[mask]
                if length > best:
                    best = length
            else:
                first[mask] = i
        return best
