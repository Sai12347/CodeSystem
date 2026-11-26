class Solution:
    def minWindow(self, s: str, t: str) -> str:
        m, n = len(s), len(t)
        if n > m:
            return ""
        req = Counter(t)
        required = len(req)
        best_start = -1
        best_len = m + 1
        for i in range(m - n + 1):
            if s[i] not in req:
                continue
            window = defaultdict(int)
            formed = 0
            limit = min(m, i + best_len - 1)
            for j in range(i, limit):
                ch = s[j]
                if ch in req:
                    window[ch] += 1
                    if window[ch] == req[ch]:
                        formed += 1
                        if formed == required:
                            best_len = j - i + 1
                            best_start = i
                            break
        return "" if best_start == -1 else s[best_start:best_start + best_len]
