class Solution {
    public int maxCircularSubarraySum(int[] nums) {
        int total = 0, maxEnd = nums[0], minEnd = nums[0], maxSum = nums[0], minSum = nums[0];
        total = nums[0];
        for (int i = 1; i < nums.length; i++) { int x = nums[i]; total += x; maxEnd = Math.max(x, maxEnd + x); maxSum = Math.max(maxSum, maxEnd); minEnd = Math.min(x, minEnd + x); minSum = Math.min(minSum, minEnd); }
        return maxSum < 0 ? maxSum : Math.max(maxSum, total - minSum);
    }
}
