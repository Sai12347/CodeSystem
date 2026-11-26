class Solution {
    public int countBetweenExtremes(int[] nums) {
        int low = nums[0], high = nums[0];
        for (int x : nums) { low = Math.min(low, x); high = Math.max(high, x); }
        int count = 0; for (int x : nums) if (low < x && x < high) count++;
        return count;
    }
}
