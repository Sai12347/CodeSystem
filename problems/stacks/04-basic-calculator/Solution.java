class Solution {
    public int calculate(String s) {
        long res = 0;
        long num = 0;
        long sign = 1;
        Deque<Long> stack = new ArrayDeque<>();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch >= '0' && ch <= '9') {
                num = num * 10 + (ch - '0');
            } else if (ch == '+') {
                res += sign * num;
                num = 0;
                sign = 1;
            } else if (ch == '-') {
                res += sign * num;
                num = 0;
                sign = -1;
            } else if (ch == '(') {
                stack.push(res);
                stack.push(sign);
                res = 0;
                sign = 1;
            } else if (ch == ')') {
                res += sign * num;
                num = 0;
                res *= stack.pop();
                res += stack.pop();
            }
        }
        return (int) (res + sign * num);
    }
}
