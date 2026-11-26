class Solution {
    public int longestArithSeqLength(int[] nums) {
        Map<Integer, Integer>[] dp = new HashMap[nums.length];
        for (int i = 0; i < nums.length; i++) dp[i] = new HashMap<>();
        int best = 2;
        for (int i = 0; i < nums.length; i++) for (int j = 0; j < i; j++) { int d = nums[i] - nums[j]; int length = dp[j].getOrDefault(d, 1) + 1; dp[i].put(d, length); best = Math.max(best, length); }
        return best;
    }
}
