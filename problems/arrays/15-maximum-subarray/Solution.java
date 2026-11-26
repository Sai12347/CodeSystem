class Solution {
    public int maxSubArray(int[] nums) {
        int cur = nums[0];
        int best = nums[0];
        for (int i = 1; i < nums.length; i++) {
            cur = Math.max(nums[i], cur + nums[i]);
            if (cur > best) {
                best = cur;
            }
        }
        return best;
    }
}
