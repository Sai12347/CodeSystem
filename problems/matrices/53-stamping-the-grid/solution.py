class Solution:
    def possibleToStamp(self, grid: List[List[int]], stampHeight: int, stampWidth: int) -> bool:
        m, n = len(grid), len(grid[0])
        h, w = stampHeight, stampWidth
        pref = [[0] * (n + 1) for _ in range(m + 1)]
        for r in range(m):
            row = grid[r]
            pr = pref[r]
            pr1 = pref[r + 1]
            for c in range(n):
                pr1[c + 1] = row[c] + pr[c + 1] + pr1[c] - pr[c]

        diff = [[0] * (n + 2) for _ in range(m + 2)]
        if h <= m and w <= n:
            for r in range(m - h + 1):
                r2 = r + h
                for c in range(n - w + 1):
                    c2 = c + w
                    if pref[r2][c2] - pref[r][c2] - pref[r2][c] + pref[r][c] == 0:
                        diff[r + 1][c + 1] += 1
                        diff[r2 + 1][c + 1] -= 1
                        diff[r + 1][c2 + 1] -= 1
                        diff[r2 + 1][c2 + 1] += 1

        for r in range(1, m + 1):
            dr = diff[r]
            dr_prev = diff[r - 1]
            row = grid[r - 1]
            for c in range(1, n + 1):
                dr[c] += dr_prev[c] + dr[c - 1] - dr_prev[c - 1]
                if row[c - 1] == 0 and dr[c] == 0:
                    return False
        return True
