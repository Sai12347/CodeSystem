class Solution {
    public boolean canConstructPalindromes(String s, int k) {
        if (k > s.length()) return false;
        int mask = 0;
        for (int i = 0; i < s.length(); i++) {
            mask ^= 1 << (s.charAt(i) - 'a');
        }
        return Integer.bitCount(mask) <= k;
    }
}
