class Solution {
    public int maximumDifference(int[] nums) {
        int low = nums[0], best = -1;
        for (int i = 1; i < nums.length; i++) { if (nums[i] > low) best = Math.max(best, nums[i] - low); low = Math.min(low, nums[i]); }
        return best;
    }
}
