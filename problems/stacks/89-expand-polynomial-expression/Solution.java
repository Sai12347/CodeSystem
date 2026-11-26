class Solution {
    public long[] expandPolynomial(String expr) {
        Deque<long[]> vals = new ArrayDeque<>();
        Deque<Character> ops = new ArrayDeque<>();
        int i = 0, n = expr.length();
        while (i < n) {
            char ch = expr.charAt(i);
            if (ch == ' ') {
                i++;
            } else if (ch == 'x') {
                vals.push(new long[]{0L, 1L});
                i++;
            } else if (ch >= '0' && ch <= '9') {
                long num = 0;
                while (i < n && expr.charAt(i) >= '0' && expr.charAt(i) <= '9') {
                    num = num * 10 + (expr.charAt(i) - '0');
                    i++;
                }
                vals.push(new long[]{num});
            } else if (ch == '(') {
                ops.push(ch);
                i++;
            } else if (ch == ')') {
                while (!ops.isEmpty() && ops.peek() != '(') {
                    applyOp(vals, ops);
                }
                ops.pop();
                i++;
            } else {
                int p = (ch == '*') ? 2 : 1;
                while (!ops.isEmpty() && ops.peek() != '(' && ((ops.peek() == '*') ? 2 : 1) >= p) {
                    applyOp(vals, ops);
                }
                ops.push(ch);
                i++;
            }
        }
        while (!ops.isEmpty()) {
            applyOp(vals, ops);
        }
        return vals.peek();
    }

    private long[] trim(long[] p) {
        int end = p.length - 1;
        while (end > 0 && p[end] == 0L) end--;
        return Arrays.copyOf(p, end + 1);
    }

    private void applyOp(Deque<long[]> vals, Deque<Character> ops) {
        char op = ops.pop();
        long[] b = vals.pop();
        long[] a = vals.pop();
        if (op == '+' || op == '-') {
            long sign = (op == '+') ? 1L : -1L;
            int m = Math.max(a.length, b.length);
            long[] res = new long[m];
            for (int k = 0; k < m; k++) {
                long va = k < a.length ? a[k] : 0L;
                long vb = k < b.length ? b[k] : 0L;
                res[k] = va + sign * vb;
            }
            vals.push(trim(res));
        } else {
            long[] res = new long[a.length + b.length - 1];
            for (int i = 0; i < a.length; i++) {
                if (a[i] == 0L) continue;
                for (int j = 0; j < b.length; j++) {
                    res[i + j] += a[i] * b[j];
                }
            }
            vals.push(trim(res));
        }
    }
}
