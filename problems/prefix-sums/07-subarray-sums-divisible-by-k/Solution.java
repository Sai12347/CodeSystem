class Solution {
    public int subarraysDivByK(int[] nums, int k) {
        int[] counts = new int[k];
        counts[0] = 1;
        int prefix = 0;
        int ans = 0;
        for (int x : nums) {
            prefix = ((prefix + x) % k + k) % k;
            ans += counts[prefix];
            counts[prefix]++;
        }
        return ans;
    }
}
