class Solution {
    public int calculate(String s) {
        int total = 0, last = 0, num = 0;
        char op = '+';
        int n = s.length();
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (ch >= '0' && ch <= '9') {
                num = num * 10 + (ch - '0');
            }
            if ((ch < '0' || ch > '9') && ch != ' ' || i == n - 1) {
                if (op == '+') {
                    total += last;
                    last = num;
                } else if (op == '-') {
                    total += last;
                    last = -num;
                } else if (op == '*') {
                    last *= num;
                } else {
                    last /= num;
                }
                op = ch;
                num = 0;
            }
        }
        return total + last;
    }
}
