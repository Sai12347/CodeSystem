class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        vowels = set("aeiou")
        cur = 0
        best = 0
        for i, ch in enumerate(s):
            if ch in vowels:
                cur += 1
            if i >= k and s[i - k] in vowels:
                cur -= 1
            if i >= k - 1 and cur > best:
                best = cur
        return best
