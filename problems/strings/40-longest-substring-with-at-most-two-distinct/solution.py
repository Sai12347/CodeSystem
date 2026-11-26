class Solution:
    def lengthOfLongestSubstringTwoDistinct(self, s: str) -> int:
        counts = {}
        left = best = 0
        for right, c in enumerate(s):
            counts[c] = counts.get(c, 0) + 1
            while len(counts) > 2:
                x = s[left]; counts[x] -= 1
                if counts[x] == 0: del counts[x]
                left += 1
            best = max(best, right - left + 1)
        return best
