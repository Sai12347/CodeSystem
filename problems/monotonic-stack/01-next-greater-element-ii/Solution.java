class Solution {
    public int[] nextGreaterElements(int[] nums) {
        int n = nums.length;
        int[] res = new int[n];
        Arrays.fill(res, -1);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < 2 * n; i++) {
            int cur = nums[i % n];
            while (!stack.isEmpty() && nums[stack.peek()] < cur) {
                res[stack.pop()] = cur;
            }
            if (i < n) {
                stack.push(i);
            }
        }
        return res;
    }
}
