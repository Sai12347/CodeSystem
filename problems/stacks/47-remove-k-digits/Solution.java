class Solution {
    public String removeKdigits(String num, int k) {
        int n = num.length();
        char[] st = new char[n];
        int top = 0;
        int rem = k;
        for (int i = 0; i < n; i++) {
            char ch = num.charAt(i);
            while (rem > 0 && top > 0 && st[top - 1] > ch) {
                top--;
                rem--;
            }
            st[top++] = ch;
        }
        top -= rem;
        int start = 0;
        while (start < top && st[start] == '0') start++;
        return start == top ? "0" : new String(st, start, top - start);
    }
}
