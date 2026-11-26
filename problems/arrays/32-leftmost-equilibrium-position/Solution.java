class Solution {
    public int equilibriumIndex(int[] nums) {
        long right = 0, left = 0;
        for (int x : nums) right += x;
        for (int i = 0; i < nums.length; i++) { right -= nums[i]; if (left == right) return i; left += nums[i]; }
        return -1;
    }
}
