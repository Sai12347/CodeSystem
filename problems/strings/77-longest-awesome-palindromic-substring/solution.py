class Solution:
    def longestAwesome(self, s: str) -> int:
        first = [len(s)] * 1024
        first[0] = -1
        mask = 0
        best = 1
        for i, ch in enumerate(s):
            mask ^= 1 << (ord(ch) - 48)
            if first[mask] == len(s):
                first[mask] = i
            else:
                best = max(best, i - first[mask])
            for d in range(10):
                p = first[mask ^ (1 << d)]
                if p < i:
                    best = max(best, i - p)
        return best
