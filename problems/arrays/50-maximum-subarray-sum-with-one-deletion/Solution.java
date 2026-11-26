class Solution {
    public int maximumSumWithOneDeletion(int[] nums) {
        int keep = nums[0], drop = 0, best = nums[0];
        for (int i = 1; i < nums.length; i++) { int x = nums[i]; drop = Math.max(keep, drop + x); keep = Math.max(x, keep + x); best = Math.max(best, Math.max(keep, drop)); }
        return best;
    }
}
