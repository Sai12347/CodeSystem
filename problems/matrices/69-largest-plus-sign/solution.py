class Solution:
    def orderOfLargestPlusSign(self, n: int, mines: List[List[int]]) -> int:
        dp = [[n] * n for _ in range(n)]
        for r, c in mines:
            dp[r][c] = 0

        for r in range(n):
            row = dp[r]
            cnt = 0
            for c in range(n):
                cnt = 0 if row[c] == 0 else cnt + 1
                if cnt < row[c]:
                    row[c] = cnt
            cnt = 0
            for c in range(n - 1, -1, -1):
                cnt = 0 if row[c] == 0 else cnt + 1
                if cnt < row[c]:
                    row[c] = cnt

        best = 0
        for c in range(n):
            cnt = 0
            for r in range(n):
                cnt = 0 if dp[r][c] == 0 else cnt + 1
                if cnt < dp[r][c]:
                    dp[r][c] = cnt
            cnt = 0
            for r in range(n - 1, -1, -1):
                cnt = 0 if dp[r][c] == 0 else cnt + 1
                if cnt < dp[r][c]:
                    dp[r][c] = cnt
                if dp[r][c] > best:
                    best = dp[r][c]
        return best
