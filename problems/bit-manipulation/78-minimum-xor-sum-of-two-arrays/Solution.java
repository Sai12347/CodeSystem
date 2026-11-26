class Solution {
    public int minimumXorSum(int[] nums1, int[] nums2) {
        int n = nums1.length;
        int size = 1 << n;
        int[] dp = new int[size];
        Arrays.fill(dp, Integer.MAX_VALUE / 2);
        dp[0] = 0;
        for (int mask = 1; mask < size; mask++) {
            int i = Integer.bitCount(mask) - 1;
            int a = nums1[i];
            int best = Integer.MAX_VALUE / 2;
            int rem = mask;
            while (rem != 0) {
                int lb = rem & -rem;
                int j = Integer.numberOfTrailingZeros(lb);
                int cand = dp[mask ^ lb] + (a ^ nums2[j]);
                if (cand < best) best = cand;
                rem ^= lb;
            }
            dp[mask] = best;
        }
        return dp[size - 1];
    }
}
