class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        best = 0
        for target in set(s):
            left = 0
            diff = 0
            for right, ch in enumerate(s):
                if ch != target:
                    diff += 1
                while diff > k:
                    if s[left] != target:
                        diff -= 1
                    left += 1
                length = right - left + 1
                if length > best:
                    best = length
        return best
