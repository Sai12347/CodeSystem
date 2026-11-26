class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        # Independent 2D DP table: dp[i][a] = ways to make sum a using first i coins
        n = len(coins)
        dp = [[0] * (amount + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = 1
        for i in range(1, n + 1):
            c = coins[i - 1]
            prev_row = dp[i - 1]
            curr_row = dp[i]
            for a in range(1, amount + 1):
                ways = prev_row[a]
                if a >= c:
                    ways += curr_row[a - c]
                curr_row[a] = ways
        return dp[n][amount]
