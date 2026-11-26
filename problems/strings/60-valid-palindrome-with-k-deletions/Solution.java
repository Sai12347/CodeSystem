class Solution {
    public boolean isValidPalindromeK(String s, int k) {
        int n = s.length();
        int[] dp = new int[n];
        for (int i = n - 1; i >= 0; i--) {
            dp[i] = 1;
            int prevDiag = 0;
            for (int j = i + 1; j < n; j++) {
                int saved = dp[j];
                if (s.charAt(i) == s.charAt(j)) {
                    dp[j] = prevDiag + 2;
                } else {
                    dp[j] = Math.max(dp[j], dp[j - 1]);
                }
                prevDiag = saved;
            }
        }
        return n - dp[n - 1] <= k;
    }
}
