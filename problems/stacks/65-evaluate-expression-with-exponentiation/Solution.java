class Solution {
    public long evalWithPower(String s) {
        Deque<Long> vals = new ArrayDeque<>();
        Deque<Character> ops = new ArrayDeque<>();
        int i = 0, n = s.length();
        while (i < n) {
            char ch = s.charAt(i);
            if (ch == ' ') {
                i++;
            } else if (ch >= '0' && ch <= '9') {
                long num = 0;
                while (i < n && s.charAt(i) >= '0' && s.charAt(i) <= '9') {
                    num = num * 10 + (s.charAt(i) - '0');
                    i++;
                }
                vals.push(num);
            } else if (ch == '(') {
                ops.push(ch);
                i++;
            } else if (ch == ')') {
                while (!ops.isEmpty() && ops.peek() != '(') {
                    applyTop(vals, ops);
                }
                ops.pop();
                i++;
            } else {
                int p = prec(ch);
                while (!ops.isEmpty() && ops.peek() != '('
                        && (prec(ops.peek()) > p || (ch != '^' && prec(ops.peek()) == p))) {
                    applyTop(vals, ops);
                }
                ops.push(ch);
                i++;
            }
        }
        while (!ops.isEmpty()) {
            applyTop(vals, ops);
        }
        return vals.peek();
    }

    private int prec(char op) {
        if (op == '+' || op == '-') return 1;
        if (op == '*') return 2;
        if (op == '^') return 3;
        return 0;
    }

    private void applyTop(Deque<Long> vals, Deque<Character> ops) {
        char op = ops.pop();
        long b = vals.pop();
        long a = vals.pop();
        if (op == '+') vals.push(a + b);
        else if (op == '-') vals.push(a - b);
        else if (op == '*') vals.push(a * b);
        else {
            long res = 1L, base = a, exp = b;
            while (exp > 0) {
                if ((exp & 1L) != 0) res *= base;
                base *= base;
                exp >>= 1;
            }
            vals.push(res);
        }
    }
}
