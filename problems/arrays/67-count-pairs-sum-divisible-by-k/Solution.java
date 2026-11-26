class Solution {
    public long countPairsDivisibleByK(int[] nums, int k) {
        long[] counts = new long[k]; long answer = 0;
        for (int x : nums) { int r = x % k; answer += counts[(k - r) % k]; counts[r]++; }
        return answer;
    }
}
