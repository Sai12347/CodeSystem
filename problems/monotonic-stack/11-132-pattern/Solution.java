class Solution {
    public boolean find132pattern(int[] nums) {
        Deque<Integer> stack = new ArrayDeque<>();
        int third = Integer.MIN_VALUE;
        boolean hasThird = false;
        for (int i = nums.length - 1; i >= 0; i--) {
            int val = nums[i];
            if (hasThird && val < third) {
                return true;
            }
            while (!stack.isEmpty() && stack.peek() < val) {
                third = stack.pop();
                hasThird = true;
            }
            stack.push(val);
        }
        return false;
    }
}
