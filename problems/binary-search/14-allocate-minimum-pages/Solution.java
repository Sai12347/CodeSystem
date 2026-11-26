class Solution {
    public int allocatePages(int[] pages, int students) {
        if (students > pages.length) {
            return -1;
        }
        long left = 0;
        long right = 0;
        for (int p : pages) {
            if (p > left) {
                left = p;
            }
            right += p;
        }
        while (left < right) {
            long mid = left + (right - left) / 2;
            int needed = 1;
            long cur = 0;
            for (int p : pages) {
                if (cur + p > mid) {
                    needed++;
                    cur = p;
                } else {
                    cur += p;
                }
            }
            if (needed <= students) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        return (int) left;
    }
}
