class Solution {
    public int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> counts = new HashMap<>();
        counts.put(0, 1);
        int prefix = 0;
        int ans = 0;
        for (int x : nums) {
            prefix += x;
            ans += counts.getOrDefault(prefix - k, 0);
            counts.put(prefix, counts.getOrDefault(prefix, 0) + 1);
        }
        return ans;
    }
}
