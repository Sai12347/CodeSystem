class Solution {
    public boolean canDivideIntoPairs(int[] nums) {
        int[] parity = new int[501];
        for (int x : nums) parity[x] ^= 1;
        for (int x : parity) if (x != 0) return false;
        return true;
    }
}
