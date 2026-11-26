class Solution {
    public int countTriplets(int[] nums) {
        int maxVal = 0;
        for (int x : nums) {
            if (x > maxVal) maxVal = x;
        }
        int n = nums.length;
        if (maxVal == 0) return n * n * n;
        int bits = 32 - Integer.numberOfLeadingZeros(maxVal);
        int size = 1 << bits;
        int full = size - 1;
        int[] freq = new int[size];
        int unique = 0;
        for (int x : nums) {
            if (freq[x]++ == 0) unique++;
        }
        int[] vals = new int[unique];
        int[] cnts = new int[unique];
        int idx = 0;
        for (int v = 0; v < size; v++) {
            if (freq[v] > 0) {
                vals[idx] = v;
                cnts[idx] = freq[v];
                idx++;
            }
        }
        int[] dp = new int[size];
        for (int i = 0; i < unique; i++) {
            int a = vals[i], ca = cnts[i];
            dp[a] += ca * ca;
            for (int j = i + 1; j < unique; j++) {
                dp[a & vals[j]] += 2 * ca * cnts[j];
            }
        }
        for (int b = 0; b < bits; b++) {
            int bit = 1 << b;
            int step = bit << 1;
            for (int start = bit; start < size; start += step) {
                for (int mask = start; mask < start + bit; mask++) {
                    dp[mask] += dp[mask ^ bit];
                }
            }
        }
        int ans = 0;
        for (int i = 0; i < unique; i++) {
            ans += cnts[i] * dp[full ^ vals[i]];
        }
        return ans;
    }
}
