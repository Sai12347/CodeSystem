class Solution {
    public int[] evalSetExpression(String expr) {
        Deque<Set<Integer>> vals = new ArrayDeque<>();
        Deque<Character> ops = new ArrayDeque<>();
        int i = 0, n = expr.length();
        while (i < n) {
            char ch = expr.charAt(i);
            if (ch == ' ') {
                i++;
            } else if (ch == '{') {
                int j = expr.indexOf('}', i);
                String inner = expr.substring(i + 1, j).trim();
                Set<Integer> s = new HashSet<>();
                if (!inner.isEmpty()) {
                    for (String part : inner.split(",")) {
                        s.add(Integer.parseInt(part.trim()));
                    }
                }
                vals.push(s);
                i = j + 1;
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
                int p = (ch == '&') ? 2 : 1;
                while (!ops.isEmpty() && ops.peek() != '(' && ((ops.peek() == '&') ? 2 : 1) >= p) {
                    applyOp(vals, ops);
                }
                ops.push(ch);
                i++;
            }
        }
        while (!ops.isEmpty()) {
            applyOp(vals, ops);
        }
        Set<Integer> resSet = vals.peek();
        int[] ans = new int[resSet.size()];
        int idx = 0;
        for (int v : resSet) ans[idx++] = v;
        Arrays.sort(ans);
        return ans;
    }

    private void applyOp(Deque<Set<Integer>> vals, Deque<Character> ops) {
        char op = ops.pop();
        Set<Integer> b = vals.pop();
        Set<Integer> a = vals.pop();
        Set<Integer> res = new HashSet<>();
        if (op == '&') {
            for (int v : a) if (b.contains(v)) res.add(v);
        } else if (op == '|') {
            res.addAll(a);
            res.addAll(b);
        } else if (op == '-') {
            for (int v : a) if (!b.contains(v)) res.add(v);
        } else {
            for (int v : a) if (!b.contains(v)) res.add(v);
            for (int v : b) if (!a.contains(v)) res.add(v);
        }
        vals.push(res);
    }
}
