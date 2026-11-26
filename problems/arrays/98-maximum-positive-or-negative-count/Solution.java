class Solution {
    public int maximumCount(int[] nums) {
        int negative = 0, positive = 0;
        for (int x : nums) { if (x < 0) negative++; else if (x > 0) positive++; }
        return Math.max(negative, positive);
    }
}
