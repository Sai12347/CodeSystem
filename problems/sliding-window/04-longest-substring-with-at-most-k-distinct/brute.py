class Solution:
    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        if k == 0:
            return 0
        n = len(s)
        best = 0
        for i in range(n):
            if n - i <= best:
                break
            seen = set()
            j = i
            while j < n:
                seen.add(s[j])
                if len(seen) > k:
                    break
                j += 1
            if j - i > best:
                best = j - i
        return best
