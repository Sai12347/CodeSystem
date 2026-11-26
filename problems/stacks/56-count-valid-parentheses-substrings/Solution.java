class Solution {
    public long countValidSubstrings(String s) {
        int n = s.length();
        long[] dp = new long[n];
        Deque<Integer> stack = new ArrayDeque<>();
        long total = 0;
        for (int i = 0; i < n; i++) {
            if (s.charAt(i) == '(') {
                stack.push(i);
            } else if (!stack.isEmpty()) {
                int j = stack.pop();
                dp[i] = 1L + (j > 0 ? dp[j - 1] : 0L);
                total += dp[i];
            }
        }
        return total;
    }
}
