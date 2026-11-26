class Solution {
    public int equalSubstring(String s, String t, int maxCost) {
        int left = 0;
        int cost = 0;
        int best = 0;
        int n = s.length();
        for (int right = 0; right < n; right++) {
            cost += Math.abs(s.charAt(right) - t.charAt(right));
            while (cost > maxCost) {
                cost -= Math.abs(s.charAt(left) - t.charAt(left));
                left++;
            }
            int len = right - left + 1;
            if (len > best) {
                best = len;
            }
        }
        return best;
    }
}
