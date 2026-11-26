class Solution {
    public String minWindow(String s, String t) {
        int m = s.length(), n = t.length();
        if (n > m) {
            return "";
        }
        int[] need = new int[128];
        for (int i = 0; i < n; i++) {
            need[t.charAt(i)]++;
        }
        int missing = n;
        int left = 0;
        int bestStart = 0;
        int bestLen = m + 1;

        for (int right = 0; right < m; right++) {
            char ch = s.charAt(right);
            if (need[ch] > 0) {
                missing--;
            }
            need[ch]--;

            while (missing == 0) {
                int len = right - left + 1;
                if (len < bestLen) {
                    bestLen = len;
                    bestStart = left;
                }
                char leftCh = s.charAt(left);
                need[leftCh]++;
                if (need[leftCh] > 0) {
                    missing++;
                }
                left++;
            }
        }
        return bestLen > m ? "" : s.substring(bestStart, bestStart + bestLen);
    }
}
