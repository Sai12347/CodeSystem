class Solution {
    public String minWindowSubsequence(String s1, String s2) {
        int n = s1.length(), m = s2.length();
        int bestStart = -1, bestLen = n + 1;
        int i = 0;
        while (i < n) {
            int j = 0;
            while (i < n) {
                if (s1.charAt(i) == s2.charAt(j)) {
                    j++;
                    if (j == m) break;
                }
                i++;
            }
            if (j < m) break;
            int end = i;
            j = m - 1;
            while (j >= 0) {
                if (s1.charAt(i) == s2.charAt(j)) j--;
                i--;
            }
            int start = i + 1;
            if (end - start + 1 < bestLen) {
                bestLen = end - start + 1;
                bestStart = start;
            }
            i = start + 1;
        }
        return bestStart == -1 ? "" : s1.substring(bestStart, bestStart + bestLen);
    }
}
