class Solution:
    def countBinarySubstrings(self, s: str) -> int:
        previous = 0
        run = 1
        total = 0
        for i in range(1, len(s)):
            if s[i] == s[i - 1]: run += 1
            else: total += min(previous, run); previous, run = run, 1
        return total + min(previous, run)
