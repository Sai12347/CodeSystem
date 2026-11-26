class Solution:
    def trapRainWater(self, heightMap: List[List[int]]) -> int:
        m, n = len(heightMap), len(heightMap[0])
        if m <= 2 or n <= 2:
            return 0
        INF = 10**9
        level = [[heightMap[r][c] if (r in (0, m - 1) or c in (0, n - 1)) else INF for c in range(n)] for r in range(m)]
        changed = True
        while changed:
            changed = False
            for r in range(1, m - 1):
                for c in range(1, n - 1):
                    nb = min(level[r - 1][c], level[r + 1][c], level[r][c - 1], level[r][c + 1])
                    new_lv = max(heightMap[r][c], nb)
                    if new_lv < level[r][c]:
                        level[r][c] = new_lv
                        changed = True
        return sum(level[r][c] - heightMap[r][c] for r in range(m) for c in range(n))
