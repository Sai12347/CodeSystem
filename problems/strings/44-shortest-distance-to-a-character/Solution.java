class Solution {
    public int[] shortestToChar(String s, String c) {
        char target = c.charAt(0);
        int n = s.length();
        int[] ans = new int[n];
        int prev = -n;
        for (int i = 0; i < n; i++) {
            if (s.charAt(i) == target) prev = i;
            ans[i] = i - prev;
        }
        prev = 2 * n;
        for (int i = n - 1; i >= 0; i--) {
            if (s.charAt(i) == target) prev = i;
            ans[i] = Math.min(ans[i], prev - i);
        }
        return ans;
    }
}
