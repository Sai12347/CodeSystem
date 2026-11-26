class Adapter {
    public static Object run(Map<String, Object> inp) {
        String s = (String) inp.get("s");
        String res = new Solution().frequencySort(s);
        if (res == null) {
            return "Expected non-null String, got null";
        }
        if (res.length() != s.length()) {
            return "Output length " + res.length() + " != input length " + s.length();
        }
        Map<Character, Integer> counts = new HashMap<>();
        for (int i = 0; i < s.length(); i++) {
            counts.merge(s.charAt(i), 1, Integer::sum);
        }
        for (int i = 0; i < res.length(); i++) {
            char ch = res.charAt(i);
            int rem = counts.getOrDefault(ch, 0) - 1;
            if (rem < 0) {
                return "Output is not a permutation of the input string";
            }
            counts.put(ch, rem);
        }
        Set<Character> seen = new HashSet<>();
        int prevRun = s.length() + 1;
        int i = 0;
        int n = res.length();
        while (i < n) {
            char ch = res.charAt(i);
            if (!seen.add(ch)) {
                return "Character '" + ch + "' is not grouped contiguously";
            }
            int j = i;
            while (j < n && res.charAt(j) == ch) {
                j++;
            }
            int runLen = j - i;
            if (runLen > prevRun) {
                return "Frequencies are not in non-increasing order at character '" + ch + "'";
            }
            prevRun = runLen;
            i = j;
        }
        return true;
    }
}
