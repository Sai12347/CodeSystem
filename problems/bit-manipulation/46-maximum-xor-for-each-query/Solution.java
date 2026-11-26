class Solution {
    public int[] getMaximumXor(int[] nums, int maximumBit) {
        int mask = (1 << maximumBit) - 1;
        int cur = 0;
        for (int v : nums) cur ^= v;
        int n = nums.length;
        int[] ans = new int[n];
        for (int i = 0; i < n; i++) {
            ans[i] = cur ^ mask;
            cur ^= nums[n - 1 - i];
        }
        return ans;
    }
}
