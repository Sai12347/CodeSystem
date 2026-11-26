class Solution {
    public int shipWithinDays(int[] weights, int days) {
        int left = 0;
        int right = 0;
        for (int w : weights) {
            if (w > left) {
                left = w;
            }
            right += w;
        }
        while (left < right) {
            int mid = left + (right - left) / 2;
            int needed = 1;
            int load = 0;
            for (int w : weights) {
                if (load + w > mid) {
                    needed++;
                    load = w;
                } else {
                    load += w;
                }
            }
            if (needed <= days) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        return left;
    }
}
