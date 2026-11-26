class Solution {
    public int evaluateMinMax(String expr) {
        Deque<Character> ops = new ArrayDeque<>();
        Deque<Integer> vals = new ArrayDeque<>();
        int i = 0, n = expr.length();
        while (i < n) {
            char ch = expr.charAt(i);
            if (ch == 'm') {
                ops.push(expr.charAt(i + 1) == 'i' ? 'n' : 'x');
                i += 4;
            } else if (ch == ',') {
                i++;
            } else if (ch == ')') {
                int b = vals.pop();
                int a = vals.pop();
                char op = ops.pop();
                vals.push(op == 'n' ? Math.min(a, b) : Math.max(a, b));
                i++;
            } else {
                int sign = 1;
                if (ch == '-') {
                    sign = -1;
                    i++;
                }
                int num = 0;
                while (i < n && expr.charAt(i) >= '0' && expr.charAt(i) <= '9') {
                    num = num * 10 + (expr.charAt(i) - '0');
                    i++;
                }
                vals.push(sign * num);
            }
        }
        return vals.pop();
    }
}
