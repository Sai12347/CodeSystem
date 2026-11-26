class Solution {
    public int minSwapsToGroupOnes(int[] nums) {
        int ones = 0; for (int x : nums) ones += x; if (ones <= 1) return 0;
        int current = 0; for (int i = 0; i < ones; i++) current += nums[i]; int best = current;
        for (int i = ones; i < nums.length; i++) { current += nums[i] - nums[i - ones]; best = Math.max(best, current); }
        return ones - best;
    }
}
