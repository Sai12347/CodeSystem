class Solution {
    public int longestCommonSubstring(String s1, String s2) {
        int m = s2.length();
        int[] dp = new int[m + 1];
        int best = 0;
        for (int i = 0; i < s1.length(); i++) {
            char ch = s1.charAt(i);
            for (int j = m; j >= 1; j--) {
                if (ch == s2.charAt(j - 1)) {
                    dp[j] = dp[j - 1] + 1;
                    if (dp[j] > best) best = dp[j];
                } else {
                    dp[j] = 0;
                }
            }
        }
        return best;
    }
}
