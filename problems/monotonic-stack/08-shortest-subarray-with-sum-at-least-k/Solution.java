class Solution {
    public int shortestSubarray(int[] nums, int k) {
        int n = nums.length;
        long[] prefix = new long[n + 1];
        for (int i = 0; i < n; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }
        Deque<Integer> dq = new ArrayDeque<>();
        int best = n + 1;
        for (int i = 0; i <= n; i++) {
            long p = prefix[i];
            while (!dq.isEmpty() && p - prefix[dq.peekFirst()] >= k) {
                int len = i - dq.pollFirst();
                if (len < best) {
                    best = len;
                }
            }
            while (!dq.isEmpty() && prefix[dq.peekLast()] >= p) {
                dq.pollLast();
            }
            dq.offerLast(i);
        }
        return best <= n ? best : -1;
    }
}
