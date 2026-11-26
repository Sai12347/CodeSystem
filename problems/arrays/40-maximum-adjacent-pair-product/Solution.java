class Solution {
    public int maximumAdjacentProduct(int[] nums) {
        int best = nums[0] * nums[1];
        for (int i = 1; i + 1 < nums.length; i++) best = Math.max(best, nums[i] * nums[i + 1]);
        return best;
    }
}
