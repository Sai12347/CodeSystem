class Solution:
    def shortestWay(self, source: str, target: str) -> int:
        m = len(source)
        nxt = [[-1] * 26 for _ in range(m + 1)]
        for i in range(m - 1, -1, -1):
            nxt[i] = nxt[i + 1][:]
            nxt[i][ord(source[i]) - 97] = i
        ans = 1
        pos = 0
        for ch in target:
            c = ord(ch) - 97
            if nxt[0][c] == -1:
                return -1
            if nxt[pos][c] == -1:
                ans += 1
                pos = 0
            pos = nxt[pos][c] + 1
        return ans
