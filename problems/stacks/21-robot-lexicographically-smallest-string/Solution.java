class Solution {
    public String robotWithString(String s) {
        int n = s.length();
        char[] sufMin = new char[n + 1];
        sufMin[n] = '{';
        for (int i = n - 1; i >= 0; i--) {
            char c = s.charAt(i);
            sufMin[i] = c < sufMin[i + 1] ? c : sufMin[i + 1];
        }
        char[] stack = new char[n];
        int top = 0;
        StringBuilder out = new StringBuilder(n);
        for (int i = 0; i < n; i++) {
            stack[top++] = s.charAt(i);
            char nxt = sufMin[i + 1];
            while (top > 0 && stack[top - 1] <= nxt) {
                out.append(stack[--top]);
            }
        }
        return out.toString();
    }
}
