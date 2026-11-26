class Solution {
    public int maximumGain(String s, int x, int y) {
        char first = x >= y ? 'a' : 'b';
        char second = x >= y ? 'b' : 'a';
        int hi = Math.max(x, y);
        int lo = Math.min(x, y);
        int score = 0;
        StringBuilder s1 = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            int len = s1.length();
            if (len > 0 && s1.charAt(len - 1) == first && ch == second) {
                s1.deleteCharAt(len - 1);
                score += hi;
            } else {
                s1.append(ch);
            }
        }
        StringBuilder s2 = new StringBuilder();
        for (int i = 0; i < s1.length(); i++) {
            char ch = s1.charAt(i);
            int len = s2.length();
            if (len > 0 && s2.charAt(len - 1) == second && ch == first) {
                s2.deleteCharAt(len - 1);
                score += lo;
            } else {
                s2.append(ch);
            }
        }
        return score;
    }
}
