class Solution {
    public int[] largestStackOutput(int[] nums) {
        int n = nums.length;
        int[] sufMax = new int[n + 1];
        for (int i = n - 1; i >= 0; i--) {
            sufMax[i] = Math.max(nums[i], sufMax[i + 1]);
        }
        Deque<Integer> stack = new ArrayDeque<>();
        int[] out = new int[n];
        int idx = 0;
        for (int i = 0; i < n; i++) {
            stack.push(nums[i]);
            int nxtMax = sufMax[i + 1];
            while (!stack.isEmpty() && stack.peek() > nxtMax) {
                out[idx++] = stack.pop();
            }
        }
        return out;
    }
}
