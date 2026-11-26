class Solution:
    def canConstructPalindromes(self, s: str, k: int) -> bool:
        if k > len(s):
            return False
        mask = 0
        for ch in s:
            mask ^= 1 << (ord(ch) - 97)
        return mask.bit_count() <= k
