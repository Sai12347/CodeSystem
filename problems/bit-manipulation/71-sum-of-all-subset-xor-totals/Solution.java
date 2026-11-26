class Solution {
    public long subsetXorSum(int[] nums) {
        long orAll = 0L;
        for (int x : nums) {
            orAll |= x;
        }
        return orAll << (nums.length - 1);
    }
}
