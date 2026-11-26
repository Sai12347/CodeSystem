class Solution {
    public int splitArray(int[] nums, int k) {
        long left = 0;
        long right = 0;
        for (int x : nums) {
            if (x > left) {
                left = x;
            }
            right += x;
        }
        while (left < right) {
            long mid = left + (right - left) / 2;
            int pieces = 1;
            long cur = 0;
            for (int x : nums) {
                if (cur + x > mid) {
                    pieces++;
                    cur = x;
                } else {
                    cur += x;
                }
            }
            if (pieces <= k) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        return (int) left;
    }
}
