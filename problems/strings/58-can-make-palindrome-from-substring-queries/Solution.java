class Solution {
    public boolean[] canMakePaliQueries(String s, int[][] queries) {
        int n = s.length();
        int[] pref = new int[n + 1];
        for (int i = 0; i < n; i++) {
            pref[i + 1] = pref[i] ^ (1 << (s.charAt(i) - 'a'));
        }
        boolean[] ans = new boolean[queries.length];
        for (int i = 0; i < queries.length; i++) {
            int l = queries[i][0], r = queries[i][1], k = queries[i][2];
            int odd = Integer.bitCount(pref[r + 1] ^ pref[l]);
            ans[i] = (odd / 2) <= k;
        }
        return ans;
    }
}
