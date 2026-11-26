class Solution {
    public int longestEqualRun(int[] nums) {
        int best = 1, run = 1;
        for (int i = 1; i < nums.length; i++) { run = nums[i] == nums[i - 1] ? run + 1 : 1; best = Math.max(best, run); }
        return best;
    }
}
