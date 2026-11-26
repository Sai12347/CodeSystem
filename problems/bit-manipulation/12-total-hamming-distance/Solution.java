class Solution {
    public int totalHammingDistance(int[] nums) {
        int n = nums.length;
        int total = 0;
        for (int b = 0; b < 31; b++) {
            int ones = 0;
            for (int v : nums) {
                ones += (v >>> b) & 1;
            }
            total += ones * (n - ones);
        }
        return total;
    }
}
