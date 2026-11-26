class Solution {
    public boolean hasAllCodes(String s, int k) {
        int need = 1 << k;
        if (s.length() - k + 1 < need) return false;
        boolean[] seen = new boolean[need];
        int mask = need - 1;
        int code = 0;
        for (int i = 0; i < s.length(); i++) {
            code = ((code << 1) & mask) | (s.charAt(i) - '0');
            if (i >= k - 1 && !seen[code]) {
                seen[code] = true;
                if (--need == 0) return true;
            }
        }
        return false;
    }
}
