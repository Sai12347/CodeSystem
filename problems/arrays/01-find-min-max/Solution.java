class Solution {
    public int[] findMinMax(int[] nums) {
        int mn = nums[0], mx = nums[0];
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] < mn) mn = nums[i];
            else if (nums[i] > mx) mx = nums[i];
        }
        return new int[]{mn, mx};
    }
}
