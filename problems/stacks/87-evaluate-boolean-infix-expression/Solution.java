class Solution {
    public boolean evalBooleanInfix(String expr) {
        Deque<Boolean> vals = new ArrayDeque<>();
        Deque<Character> ops = new ArrayDeque<>();
        for (int i = 0; i < expr.length(); i++) {
            char ch = expr.charAt(i);
            if (ch == ' ') continue;
            if (ch == 'T') {
                vals.push(true);
            } else if (ch == 'F') {
                vals.push(false);
            } else if (ch == '(' || ch == '!') {
                ops.push(ch);
            } else if (ch == ')') {
                while (!ops.isEmpty() && ops.peek() != '(') {
                    applyOp(vals, ops);
                }
                ops.pop();
            } else {
                int p = prec(ch);
                while (!ops.isEmpty() && ops.peek() != '(' && prec(ops.peek()) >= p) {
                    applyOp(vals, ops);
                }
                ops.push(ch);
            }
        }
        while (!ops.isEmpty()) {
            applyOp(vals, ops);
        }
        return vals.peek();
    }

    private int prec(char op) {
        if (op == '|') return 1;
        if (op == '^') return 2;
        if (op == '&') return 3;
        if (op == '!') return 4;
        return 0;
    }

    private void applyOp(Deque<Boolean> vals, Deque<Character> ops) {
        char op = ops.pop();
        if (op == '!') {
            vals.push(!vals.pop());
        } else {
            boolean b = vals.pop();
            boolean a = vals.pop();
            if (op == '&') vals.push(a && b);
            else if (op == '|') vals.push(a || b);
            else vals.push(a ^ b);
        }
    }
}
