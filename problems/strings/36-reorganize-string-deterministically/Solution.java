class Solution {
    public String reorganizeString(String s) {
        int[] count = new int[26]; for (char c : s.toCharArray()) count[c-'a']++;
        StringBuilder out = new StringBuilder(); char previous = 0;
        while (out.length() < s.length()) { int pick = -1; for (int c = 0; c < 26; c++) if (count[c] > 0 && 'a'+c != previous && (pick < 0 || count[c] > count[pick])) pick = c; if (pick < 0) return ""; previous = (char)('a'+pick); out.append(previous); count[pick]--; }
        return out.toString();
    }
}
