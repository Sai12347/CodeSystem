class Solution {
    public int minOperationsForXor(int[] nums, int k) {
        int diff = k;
        for (int v : nums) {
            diff ^= v;
        }
        return Integer.bitCount(diff);
    }
}
