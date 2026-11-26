class Solution {
    public int maxResult(int[] nums, int k) {
        Deque<int[]> dq = new ArrayDeque<>();
        dq.offerLast(new int[]{0, nums[0]});
        for (int i = 1; i < nums.length; i++) {
            while (dq.peekFirst()[0] < i - k) {
                dq.pollFirst();
            }
            int cur = nums[i] + dq.peekFirst()[1];
            while (!dq.isEmpty() && dq.peekLast()[1] <= cur) {
                dq.pollLast();
            }
            dq.offerLast(new int[]{i, cur});
        }
        return dq.peekLast()[1];
    }
}
