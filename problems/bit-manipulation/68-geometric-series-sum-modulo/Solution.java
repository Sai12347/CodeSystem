class Solution {
    public long geometricSeriesMod(long a, long n, long mod) {
        long ans = 0L;
        long curSum = 1L % mod;
        long curPow = a % mod;
        long rem = n;
        while (rem > 0L) {
            if ((rem & 1L) != 0L) {
                ans = (ans * curPow + curSum) % mod;
            }
            curSum = (curSum * (1L + curPow)) % mod;
            curPow = (curPow * curPow) % mod;
            rem >>= 1;
        }
        return ans;
    }
}
