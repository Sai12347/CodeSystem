class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        n = len(s)
        best = 0
        for i in range(n):
            if n - i <= best:
                break
            seen = set()
            for j in range(i, n):
                if s[j] in seen:
                    break
                seen.add(s[j])
            if len(seen) > best:
                best = len(seen)
        return best
