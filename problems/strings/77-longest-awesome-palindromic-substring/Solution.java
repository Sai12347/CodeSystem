class Solution {
    public int longestAwesome(String s) {
        int n = s.length();
        int[] first = new int[1024];
        Arrays.fill(first, n);
        first[0] = -1;
        int mask = 0, best = 1;
        for (int i = 0; i < n; i++) {
            mask ^= 1 << (s.charAt(i) - '0');
            if (first[mask] == n) first[mask] = i;
            else best = Math.max(best, i - first[mask]);
            for (int d = 0; d < 10; d++) {
                int p = first[mask ^ (1 << d)];
                if (p < i) best = Math.max(best, i - p);
            }
        }
        return best;
    }
}
