class Solution {
    public List<String> restoreIpAddresses(String s) {
        int n = s.length();
        List<String> res = new ArrayList<>();
        if (n < 4 || n > 12) return res;
        String[] parts = new String[4];
        backtrack(s, n, 0, 0, parts, res);
        return res;
    }

    private void backtrack(String s, int n, int start, int seg, String[] parts, List<String> res) {
        int remChars = n - start;
        int remSegs = 4 - seg;
        if (remChars < remSegs || remChars > 3 * remSegs) return;
        if (seg == 4) {
            res.add(parts[0] + "." + parts[1] + "." + parts[2] + "." + parts[3]);
            return;
        }
        int val = 0;
        int maxLen = Math.min(3, remChars);
        for (int len = 1; len <= maxLen; len++) {
            if (len > 1 && s.charAt(start) == '0') break;
            val = val * 10 + (s.charAt(start + len - 1) - '0');
            if (val > 255) break;
            parts[seg] = s.substring(start, start + len);
            backtrack(s, n, start + len, seg + 1, parts, res);
        }
    }
}
