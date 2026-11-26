class Solution {
    public int superPow(int a, int[] b) {
        final int MOD = 1337;
        int base = a % MOD;
        int ans = 1;
        for (int d : b) {
            int p10 = 1;
            int cur = ans;
            int e = 10;
            while (e > 0) {
                if ((e & 1) == 1) p10 = (p10 * cur) % MOD;
                cur = (cur * cur) % MOD;
                e >>= 1;
            }
            int pd = 1;
            cur = base;
            e = d;
            while (e > 0) {
                if ((e & 1) == 1) pd = (pd * cur) % MOD;
                cur = (cur * cur) % MOD;
                e >>= 1;
            }
            ans = (p10 * pd) % MOD;
        }
        return ans;
    }
}
