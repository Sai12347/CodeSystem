class Solution:
    def longestPalindrome(self, s: str) -> str:
        # Manacher's algorithm: O(n) time, O(n) space
        t = "^#" + "#".join(s) + "#$"
        m = len(t)
        p = [0] * m
        center = right = 0
        best_len = 0
        best_center = 0

        for i in range(1, m - 1):
            mirror = 2 * center - i
            if i < right:
                p[i] = min(right - i, p[mirror])
            while t[i + 1 + p[i]] == t[i - 1 - p[i]]:
                p[i] += 1
            if i + p[i] > right:
                center = i
                right = i + p[i]
            if p[i] > best_len:
                best_len = p[i]
                best_center = i

        start = (best_center - best_len) // 2
        return s[start:start + best_len]
