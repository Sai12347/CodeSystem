class Solution {
    public String customSortString(String order, String s) {
        int[] counts = new int[26];
        for (int i = 0; i < s.length(); i++) {
            counts[s.charAt(i) - 'a']++;
        }
        StringBuilder sb = new StringBuilder(s.length());
        for (int i = 0; i < order.length(); i++) {
            char ch = order.charAt(i);
            int idx = ch - 'a';
            while (counts[idx] > 0) {
                sb.append(ch);
                counts[idx]--;
            }
        }
        for (int idx = 0; idx < 26; idx++) {
            char ch = (char) ('a' + idx);
            while (counts[idx] > 0) {
                sb.append(ch);
                counts[idx]--;
            }
        }
        return sb.toString();
    }
}
