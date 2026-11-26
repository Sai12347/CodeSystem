class Solution {
    public String longestNiceSubstring(String s) {
        int[] res = solve(s, 0, s.length());
        return s.substring(res[0], res[1]);
    }
    private int[] solve(String s, int l, int r) {
        if (r - l < 2) return new int[]{0, 0};
        int lower = 0, upper = 0;
        for (int i = l; i < r; i++) {
            char c = s.charAt(i);
            if (c >= 'a') lower |= 1 << (c - 'a');
            else upper |= 1 << (c - 'A');
        }
        int good = lower & upper;
        int start = l;
        int[] best = {0, 0};
        boolean hasBad = false;
        for (int i = l; i < r; i++) {
            char c = s.charAt(i);
            int bit = 1 << (c >= 'a' ? c - 'a' : c - 'A');
            if ((good & bit) == 0) {
                hasBad = true;
                int[] cand = solve(s, start, i);
                if (cand[1] - cand[0] > best[1] - best[0]) best = cand;
                start = i + 1;
            }
        }
        if (!hasBad) return new int[]{l, r};
        int[] cand = solve(s, start, r);
        if (cand[1] - cand[0] > best[1] - best[0]) best = cand;
        return best;
    }
}
