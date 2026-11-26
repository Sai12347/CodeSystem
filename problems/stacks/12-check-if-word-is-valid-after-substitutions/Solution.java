class Solution {
    public boolean isValid(String s) {
        int n = s.length();
        if (n % 3 != 0) {
            return false;
        }
        char[] stack = new char[n];
        int top = 0;
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (ch == 'c') {
                if (top < 2 || stack[top - 1] != 'b' || stack[top - 2] != 'a') {
                    return false;
                }
                top -= 2;
            } else {
                stack[top++] = ch;
            }
        }
        return top == 0;
    }
}
