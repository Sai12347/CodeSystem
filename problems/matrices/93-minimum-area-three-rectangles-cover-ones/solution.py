class Solution:
    def minimumSumThreeRectangles(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        ps = [[0] * (n + 1) for _ in range(m + 1)]
        for r in range(m):
            row_sum = 0
            for c in range(n):
                row_sum += grid[r][c]
                ps[r + 1][c + 1] = ps[r][c + 1] + row_sum

        INF = 10**9

        def ones(r1: int, r2: int, c1: int, c2: int) -> int:
            return ps[r2 + 1][c2 + 1] - ps[r1][c2 + 1] - ps[r2 + 1][c1] + ps[r1][c1]

        def bbox(r1: int, r2: int, c1: int, c2: int) -> int:
            if ones(r1, r2, c1, c2) == 0:
                return INF
            top = r1
            while ones(top, top, c1, c2) == 0:
                top += 1
            bot = r2
            while ones(bot, bot, c1, c2) == 0:
                bot -= 1
            left = c1
            while ones(top, bot, left, left) == 0:
                left += 1
            right = c2
            while ones(top, bot, right, right) == 0:
                right -= 1
            return (bot - top + 1) * (right - left + 1)

        ans = INF
        # 1. Two horizontal cuts
        for r1 in range(m - 2):
            a1 = bbox(0, r1, 0, n - 1)
            if a1 >= ans:
                continue
            for r2 in range(r1 + 1, m - 1):
                cur = a1 + bbox(r1 + 1, r2, 0, n - 1) + bbox(r2 + 1, m - 1, 0, n - 1)
                if cur < ans:
                    ans = cur
        # 2. Two vertical cuts
        for c1 in range(n - 2):
            a1 = bbox(0, m - 1, 0, c1)
            if a1 >= ans:
                continue
            for c2 in range(c1 + 1, n - 1):
                cur = a1 + bbox(0, m - 1, c1 + 1, c2) + bbox(0, m - 1, c2 + 1, n - 1)
                if cur < ans:
                    ans = cur
        # 3-6. Four T-shaped cuts
        for r in range(m - 1):
            top_full = bbox(0, r, 0, n - 1)
            bot_full = bbox(r + 1, m - 1, 0, n - 1)
            for c in range(n - 1):
                tl = bbox(0, r, 0, c)
                tr = bbox(0, r, c + 1, n - 1)
                bl = bbox(r + 1, m - 1, 0, c)
                br = bbox(r + 1, m - 1, c + 1, n - 1)
                left_full = bbox(0, m - 1, 0, c)
                right_full = bbox(0, m - 1, c + 1, n - 1)
                cand = min(
                    top_full + bl + br,
                    tl + tr + bot_full,
                    left_full + tr + br,
                    tl + bl + right_full,
                )
                if cand < ans:
                    ans = cand
        return ans
