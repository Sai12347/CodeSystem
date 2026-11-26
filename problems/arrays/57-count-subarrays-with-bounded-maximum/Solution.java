class Solution {
    public long numSubarrayBoundedMax(int[] nums, int bound) {
        long total = 0; int run = 0;
        for (int x : nums) { run = x <= bound ? run + 1 : 0; total += run; }
        return total;
    }
}
