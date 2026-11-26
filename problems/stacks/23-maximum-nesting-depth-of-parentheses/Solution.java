class Solution {
    public int maxDepth(String s) {
        int cur = 0, best = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(') {
                cur++;
                if (cur > best) best = cur;
            } else if (ch == ')') {
                cur--;
            }
        }
        return best;
    }
}
