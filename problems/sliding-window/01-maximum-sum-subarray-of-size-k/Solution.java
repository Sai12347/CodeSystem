class Solution {
    public int maxSubarraySum(int[] nums, int k) {
        int windowSum = 0;
        for (int i = 0; i < k; i++) {
            windowSum += nums[i];
        }
        int best = windowSum;
        for (int i = k; i < nums.length; i++) {
            windowSum += nums[i] - nums[i - k];
            if (windowSum > best) {
                best = windowSum;
            }
        }
        return best;
    }
}
