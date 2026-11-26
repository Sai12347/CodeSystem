class Solution:
    def balancedString(self, s: str) -> int:
        n = len(s)
        target = n // 4
        idx = {"Q": 0, "W": 1, "E": 2, "R": 3}
        pref = [[0] * (n + 1) for _ in range(4)]
        for i, ch in enumerate(s):
            for c in range(4):
                pref[c][i + 1] = pref[c][i]
            pref[idx[ch]][i + 1] += 1

        tot = [pref[c][n] for c in range(4)]
        if all(t <= target for t in tot):
            return 0

        need = [max(0, t - target) for t in tot]
        min_len = sum(need)
        for length in range(min_len, n + 1):
            for i in range(n - length + 1):
                j = i + length
                if (
                    pref[0][j] - pref[0][i] >= need[0]
                    and pref[1][j] - pref[1][i] >= need[1]
                    and pref[2][j] - pref[2][i] >= need[2]
                    and pref[3][j] - pref[3][i] >= need[3]
                ):
                    return length
        return n
