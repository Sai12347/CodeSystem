class Solution {
    public int evaluateLisp(String expression) {
        this.s = expression;
        this.idx = 0;
        this.scopes = new ArrayList<>();
        return evalExpr();
    }

    private String s;
    private int idx;
    private List<Map<String, Integer>> scopes;

    private int lookup(String var) {
        for (int i = scopes.size() - 1; i >= 0; i--) {
            Integer v = scopes.get(i).get(var);
            if (v != null) return v;
        }
        return 0;
    }

    private String readToken() {
        int start = idx;
        while (idx < s.length() && s.charAt(idx) != ' ' && s.charAt(idx) != ')') {
            idx++;
        }
        return s.substring(start, idx);
    }

    private int evalAtom(String tok) {
        char c = tok.charAt(0);
        if (c == '-' || (c >= '0' && c <= '9')) {
            return Integer.parseInt(tok);
        }
        return lookup(tok);
    }

    private int evalExpr() {
        if (s.charAt(idx) != '(') {
            return evalAtom(readToken());
        }
        idx++; // skip '('
        String op = readToken();
        idx++; // skip ' '
        if (op.equals("add")) {
            int a = evalExpr();
            idx++;
            int b = evalExpr();
            idx++;
            return a + b;
        }
        if (op.equals("mult")) {
            int a = evalExpr();
            idx++;
            int b = evalExpr();
            idx++;
            return a * b;
        }
        scopes.add(new HashMap<>());
        while (true) {
            if (s.charAt(idx) == '(') {
                int res = evalExpr();
                idx++;
                scopes.remove(scopes.size() - 1);
                return res;
            }
            String tok = readToken();
            if (s.charAt(idx) == ')') {
                int res = evalAtom(tok);
                idx++;
                scopes.remove(scopes.size() - 1);
                return res;
            }
            idx++;
            int val = evalExpr();
            scopes.get(scopes.size() - 1).put(tok, val);
            idx++;
        }
    }
}
