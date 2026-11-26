class Solution:
    def longestDupSubstringLength(self, s: str) -> int:
        n = len(s)
        if n <= 1:
            return 0
        m1, m2 = 1000000007, 1000000009
        b1, b2 = 31, 37
        h1 = [0] * (n + 1)
        h2 = [0] * (n + 1)
        p1 = [1] * (n + 1)
        p2 = [1] * (n + 1)
        for i, ch in enumerate(s):
            v = ord(ch) - 96
            h1[i + 1] = (h1[i] * b1 + v) % m1
            h2[i + 1] = (h2[i] * b2 + v) % m2
            p1[i + 1] = (p1[i] * b1) % m1
            p2[i + 1] = (p2[i] * b2) % m2

        def has_dup(length: int) -> bool:
            seen = set()
            pw1, pw2 = p1[length], p2[length]
            for i in range(n - length + 1):
                x1 = (h1[i + length] - h1[i] * pw1) % m1
                x2 = (h2[i + length] - h2[i] * pw2) % m2
                key = (x1 << 32) ^ x2
                if key in seen:
                    return True
                seen.add(key)
            return False

        lo, hi = 0, n - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if has_dup(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
