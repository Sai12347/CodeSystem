class Solution {
    public int balancedString(String s) {
        int n = s.length();
        int target = n / 4;
        int[] cnt = new int[128];
        for (int i = 0; i < n; i++) {
            cnt[s.charAt(i)]++;
        }

        if (cnt['Q'] <= target && cnt['W'] <= target && cnt['E'] <= target && cnt['R'] <= target) {
            return 0;
        }

        int best = n;
        int left = 0;
        for (int right = 0; right < n; right++) {
            cnt[s.charAt(right)]--;
            while (left <= right
                    && cnt['Q'] <= target
                    && cnt['W'] <= target
                    && cnt['E'] <= target
                    && cnt['R'] <= target) {
                int len = right - left + 1;
                if (len < best) {
                    best = len;
                }
                cnt[s.charAt(left)]++;
                left++;
            }
        }

        return best;
    }
}
