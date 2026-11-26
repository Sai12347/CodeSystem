class Solution {
    public String postfixToInfix(String expr) {
        Deque<String> exprSt = new ArrayDeque<>();
        Deque<Integer> precSt = new ArrayDeque<>();
        for (String tok : expr.split(" ")) {
            if (tok.equals("+") || tok.equals("-") || tok.equals("*")) {
                int p = tok.equals("*") ? 2 : 1;
                String rStr = exprSt.pop();
                int rP = precSt.pop();
                String lStr = exprSt.pop();
                int lP = precSt.pop();
                if (lP < p) lStr = "(" + lStr + ")";
                if (rP < p || (rP == p && tok.equals("-"))) rStr = "(" + rStr + ")";
                exprSt.push(lStr + tok + rStr);
                precSt.push(p);
            } else {
                exprSt.push(tok);
                precSt.push(3);
            }
        }
        return exprSt.peek();
    }
}
