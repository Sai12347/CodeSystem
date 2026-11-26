class Solution:
    def longestPalindrome(self, s: str) -> int:
        counts=Counter(s)
        pairs=sum((v//2)*2 for v in counts.values())
        return pairs + int(pairs < len(s))
