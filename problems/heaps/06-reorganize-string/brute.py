class Solution:
    def reorganizeString(self, s: str) -> str:
        n = len(s)
        counts = Counter(s)
        if max(counts.values()) > (n + 1) // 2:
            return ""
        res = [""] * n
        idx = 0
        for ch, cnt in sorted(counts.items(), key=lambda x: -x[1]):
            for _ in range(cnt):
                if idx >= n:
                    idx = 1
                res[idx] = ch
                idx += 2
        return "".join(res)
