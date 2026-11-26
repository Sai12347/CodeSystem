class Solution {
    public int minLength(String s) {
        char[] st = new char[s.length()];
        int top = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (top > 0 && ((st[top - 1] == 'A' && ch == 'B') || (st[top - 1] == 'C' && ch == 'D'))) {
                top--;
            } else {
                st[top++] = ch;
            }
        }
        return top;
    }
}
