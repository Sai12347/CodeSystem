class Solution {
    public int coinChange(int[] coins, int amount) {
        int inf = amount + 1;
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, inf);
        dp[0] = 0;

        for (int coin : coins) {
            if (coin <= amount) {
                for (int a = coin; a <= amount; a++) {
                    if (dp[a - coin] + 1 < dp[a]) {
                        dp[a] = dp[a - coin] + 1;
                    }
                }
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }
}
