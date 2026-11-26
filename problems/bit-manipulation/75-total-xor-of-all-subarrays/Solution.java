class Solution {
    public int totalSubarrayXor(int[] nums) {
        int n = nums.length;
        if ((n & 1) == 0) return 0;
        int ans = 0;
        for (int i = 0; i < n; i += 2) {
            ans ^= nums[i];
        }
        return ans;
    }
}
