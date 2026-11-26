class Solution:
    def distinctEchoSubstrings(self, text: str) -> int:
        n = len(text)
        m1, m2 = 1000000007, 1000000009
        b1, b2 = 31, 37
        h1 = [0] * (n + 1)
        h2 = [0] * (n + 1)
        p1 = [1] * (n + 1)
        p2 = [1] * (n + 1)
        for i, ch in enumerate(text):
            v = ord(ch) - 96
            h1[i + 1] = (h1[i] * b1 + v) % m1
            h2[i + 1] = (h2[i] * b2 + v) % m2
            p1[i + 1] = (p1[i] * b1) % m1
            p2[i + 1] = (p2[i] * b2) % m2
        seen = set()
        for half in range(1, n // 2 + 1):
            pw1, pw2 = p1[half], p2[half]
            for i in range(n - 2 * half + 1):
                a1 = (h1[i + half] - h1[i] * pw1) % m1
                b1v = (h1[i + 2 * half] - h1[i + half] * pw1) % m1
                if a1 == b1v:
                    a2 = (h2[i + half] - h2[i] * pw2) % m2
                    b2v = (h2[i + 2 * half] - h2[i + half] * pw2) % m2
                    if a2 == b2v:
                        seen.add((half, a1, a2))
        return len(seen)
