class Solution {
    public int countHomogenous(String s) {
        final int MOD = 1000000007;
        long ans = 0;
        int run = 0;
        char prev = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == prev) run++;
            else { run = 1; prev = ch; }
            ans = (ans + run) % MOD;
        }
        return (int) ans;
    }
}
