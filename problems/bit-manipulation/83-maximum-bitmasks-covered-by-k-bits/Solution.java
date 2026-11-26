class Solution {
    public int maxCoveredBitmasks(int[] masks, int m, int k) {
        int size = 1 << m;
        int[] dp = new int[size];
        for (int x : masks) {
            dp[x]++;
        }
        for (int b = 0; b < m; b++) {
            int bit = 1 << b;
            int step = bit << 1;
            for (int start = bit; start < size; start += step) {
                for (int mask = start; mask < start + bit; mask++) {
                    dp[mask] += dp[mask ^ bit];
                }
            }
        }
        int ans = 0;
        for (int s = 0; s < size; s++) {
            if (Integer.bitCount(s) == k && dp[s] > ans) {
                ans = dp[s];
            }
        }
        return ans;
    }
}
