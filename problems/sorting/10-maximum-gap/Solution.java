class Solution {
    public int maximumGap(int[] nums) {
        int n = nums.length;
        if (n < 2) {
            return 0;
        }
        int mn = Integer.MAX_VALUE, mx = Integer.MIN_VALUE;
        for (int x : nums) {
            if (x < mn) mn = x;
            if (x > mx) mx = x;
        }
        if (mn == mx) {
            return 0;
        }
        int bucketSize = Math.max(1, (mx - mn) / (n - 1));
        int bucketCount = (mx - mn) / bucketSize + 1;
        int[] bMin = new int[bucketCount];
        int[] bMax = new int[bucketCount];
        boolean[] used = new boolean[bucketCount];
        Arrays.fill(bMin, Integer.MAX_VALUE);
        Arrays.fill(bMax, Integer.MIN_VALUE);
        for (int x : nums) {
            int idx = (x - mn) / bucketSize;
            used[idx] = true;
            if (x < bMin[idx]) bMin[idx] = x;
            if (x > bMax[idx]) bMax[idx] = x;
        }
        int maxGap = 0;
        int prevMax = mn;
        for (int i = 0; i < bucketCount; i++) {
            if (!used[i]) {
                continue;
            }
            maxGap = Math.max(maxGap, bMin[i] - prevMax);
            prevMax = bMax[i];
        }
        return maxGap;
    }
}
