class Adapter {
    public static Object run(Map<String, Object> inp) {
        String s = (String) inp.get("s");
        String res = new Solution().reorganizeString(s);
        if (res == null) {
            return "Expected non-null String, got null";
        }
        int n = s.length();
        int[] cnt = new int[26];
        int maxFreq = 0;
        for (int i = 0; i < n; i++) {
            int f = ++cnt[s.charAt(i) - 'a'];
            if (f > maxFreq) maxFreq = f;
        }
        boolean possible = maxFreq <= (n + 1) / 2;
        if (!possible) {
            if (res.isEmpty()) return true;
            return "Expected empty string for impossible input";
        }
        if (res.length() != n) {
            return "Output length " + res.length() + " != input length " + n;
        }
        for (int i = 0; i < n; i++) {
            char ch = res.charAt(i);
            if (ch < 'a' || ch > 'z' || --cnt[ch - 'a'] < 0) {
                return "Output is not a permutation of the input string";
            }
            if (i > 0 && res.charAt(i) == res.charAt(i - 1)) {
                return "Adjacent duplicate character '" + ch + "' at indices " + (i - 1) + " and " + i;
            }
        }
        return true;
    }
}
