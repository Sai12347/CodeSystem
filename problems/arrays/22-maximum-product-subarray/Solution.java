class Solution {
    public int maxProduct(int[] nums) {
        int high = nums[0], low = nums[0], best = nums[0];
        for (int i = 1; i < nums.length; i++) {
            int x = nums[i];
            if (x < 0) { int t = high; high = low; low = t; }
            high = Math.max(x, high * x);
            low = Math.min(x, low * x);
            best = Math.max(best, high);
        }
        return best;
    }
}
