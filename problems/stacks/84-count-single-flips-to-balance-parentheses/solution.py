class Solution:
    def countSingleFlips(self, s: str) -> int:
        n = len(s)
        pref = [0] * n
        cur = 0
        for i, ch in enumerate(s):
            cur += 1 if ch == '(' else -1
            pref[i] = cur
        total = cur
        if total != 2 and total != -2:
            return 0
        suf_min = [0] * n
        suf_min[-1] = pref[-1]
        for i in range(n - 2, -1, -1):
            suf_min[i] = pref[i] if pref[i] < suf_min[i + 1] else suf_min[i + 1]
        target_ch = '(' if total == 2 else ')'
        need_suf = 2 if total == 2 else -2
        ans = 0
        pref_min = 0
        for i in range(n):
            if pref_min >= 0 and s[i] == target_ch and suf_min[i] >= need_suf:
                ans += 1
            if pref[i] < pref_min:
                pref_min = pref[i]
        return ans
