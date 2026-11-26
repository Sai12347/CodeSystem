class Solution {
    public int constrainedSubsetSum(int[] nums, int k) {
        int n = nums.length;
        int[] dp = new int[n];
        Deque<Integer> dq = new ArrayDeque<>();
        int best = Integer.MIN_VALUE;
        for (int i = 0; i < n; i++) {
            while (!dq.isEmpty() && dq.peekFirst() < i - k) {
                dq.pollFirst();
            }
            int prev = (!dq.isEmpty() && dp[dq.peekFirst()] > 0) ? dp[dq.peekFirst()] : 0;
            dp[i] = nums[i] + prev;
            if (dp[i] > best) {
                best = dp[i];
            }
            while (!dq.isEmpty() && dp[dq.peekLast()] <= dp[i]) {
                dq.pollLast();
            }
            dq.offerLast(i);
        }
        return best;
    }
}
