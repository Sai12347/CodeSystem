class Solution:
    def partition(self, s: str) -> List[List[str]]:
        n = len(s)
        res: List[List[str]] = []
        for mask in range(1 << (n - 1)):
            parts: List[str] = []
            start = 0
            ok = True
            for i in range(n - 1):
                if mask & (1 << i):
                    sub = s[start : i + 1]
                    if sub != sub[::-1]:
                        ok = False
                        break
                    parts.append(sub)
                    start = i + 1
            if ok:
                sub = s[start:]
                if sub == sub[::-1]:
                    parts.append(sub)
                    res.append(parts)
        return res
