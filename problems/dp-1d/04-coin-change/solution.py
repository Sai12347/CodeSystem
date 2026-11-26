class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        inf = amount + 1
        dp = [inf] * (amount + 1)
        dp[0] = 0
        for coin in coins:
            if coin <= amount:
                for a in range(coin, amount + 1):
                    cand = dp[a - coin] + 1
                    if cand < dp[a]:
                        dp[a] = cand
        return dp[amount] if dp[amount] <= amount else -1
