class Solution {
    public long countSubarraysWithXor(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        freq.put(0, 1);
        int pref = 0;
        long ans = 0L;
        for (int x : nums) {
            pref ^= x;
            ans += freq.getOrDefault(pref ^ k, 0);
            freq.put(pref, freq.getOrDefault(pref, 0) + 1);
        }
        return ans;
    }
}
