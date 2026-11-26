class Adapter {
    public static Object run(Map<String, Object> inp) {
        String order = (String) inp.get("order");
        String s = (String) inp.get("s");
        String res = new Solution().customSortString(order, s);
        if (res == null) {
            return "Expected non-null String, got null";
        }
        if (res.length() != s.length()) {
            return "Output length " + res.length() + " != input length " + s.length();
        }
        int[] cnt = new int[26];
        for (int i = 0; i < s.length(); i++) {
            cnt[s.charAt(i) - 'a']++;
        }
        for (int i = 0; i < res.length(); i++) {
            char ch = res.charAt(i);
            if (ch < 'a' || ch > 'z' || --cnt[ch - 'a'] < 0) {
                return "Output is not a permutation of s";
            }
        }
        int[] rank = new int[26];
        Arrays.fill(rank, -1);
        for (int i = 0; i < order.length(); i++) {
            rank[order.charAt(i) - 'a'] = i;
        }
        int prev = -1;
        for (int i = 0; i < res.length(); i++) {
            char ch = res.charAt(i);
            int r = rank[ch - 'a'];
            if (r != -1) {
                if (r < prev) {
                    return "Character '" + ch + "' violates custom order '" + order + "'";
                }
                prev = r;
            }
        }
        return true;
    }
}
