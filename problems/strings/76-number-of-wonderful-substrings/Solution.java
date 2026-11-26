class Solution {
    public long wonderfulSubstrings(String word) {
        long[] cnt = new long[1024];
        cnt[0] = 1;
        int mask = 0;
        long ans = 0;
        for (int i = 0; i < word.length(); i++) {
            mask ^= 1 << (word.charAt(i) - 'a');
            ans += cnt[mask];
            for (int b = 0; b < 10; b++) {
                ans += cnt[mask ^ (1 << b)];
            }
            cnt[mask]++;
        }
        return ans;
    }
}
