class Solution {
    public long countWithKSetBits(long n, int k) {
        if (k == 0) return 1L;
        final int MAX_B = 60;
        long[][] comb = new long[MAX_B + 1][MAX_B + 1];
        for (int i = 0; i <= MAX_B; i++) {
            comb[i][0] = 1L;
            for (int j = 1; j <= i; j++) {
                comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j];
            }
        }
        long ans = 0L;
        int rem = k;
        for (int b = MAX_B - 1; b >= 0; b--) {
            if (((n >> b) & 1L) != 0L) {
                if (rem >= 0 && rem <= b) {
                    ans += comb[b][rem];
                }
                rem--;
                if (rem < 0) break;
            }
        }
        if (rem == 0) ans++;
        return ans;
    }
}
