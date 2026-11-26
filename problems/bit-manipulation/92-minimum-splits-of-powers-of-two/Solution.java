class Solution {
    public int minOperationsToFormTarget(int[] nums, int target) {
        long total = 0L;
        int[] cnt = new int[32];
        for (int x : nums) {
            total += x;
            cnt[Integer.numberOfTrailingZeros(x)]++;
        }
        if (total < target) return -1;
        int ops = 0;
        for (int b = 0; b < 31; b++) {
            if (((target >> b) & 1) != 0) {
                if (cnt[b] > 0) {
                    cnt[b]--;
                } else {
                    int j = b + 1;
                    while (cnt[j] == 0) j++;
                    cnt[j]--;
                    for (int m = b; m < j; m++) {
                        cnt[m]++;
                    }
                    ops += j - b;
                }
            }
            cnt[b + 1] += cnt[b] / 2;
        }
        return ops;
    }
}
