class Solution:
    def countSubstrings(self, s: str) -> int:
        t = "^#" + "#".join(s) + "#$"
        n = len(t)
        p = [0] * n
        center = 0
        right = 0
        total = 0
        for i in range(1, n - 1):
            if i < right:
                mirror = 2 * center - i
                p[i] = min(right - i, p[mirror])
            while t[i + 1 + p[i]] == t[i - 1 - p[i]]:
                p[i] += 1
            if i + p[i] > right:
                center = i
                right = i + p[i]
            total += (p[i] + 1) // 2
        return total
