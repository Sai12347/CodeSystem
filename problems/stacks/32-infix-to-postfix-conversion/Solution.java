class Solution {
    public List<String> infixToPostfix(String[] tokens) {
        List<String> out = new ArrayList<>();
        Deque<String> ops = new ArrayDeque<>();
        for (String tok : tokens) {
            if (tok.equals("(")) {
                ops.push(tok);
            } else if (tok.equals(")")) {
                while (!ops.isEmpty() && !ops.peek().equals("(")) {
                    out.add(ops.pop());
                }
                ops.pop();
            } else if (tok.equals("+") || tok.equals("-") || tok.equals("*") || tok.equals("/") || tok.equals("^")) {
                int p = tok.equals("^") ? 3 : (tok.equals("*") || tok.equals("/") ? 2 : 1);
                while (!ops.isEmpty() && !ops.peek().equals("(")) {
                    String top = ops.peek();
                    int tp = top.equals("^") ? 3 : (top.equals("*") || top.equals("/") ? 2 : 1);
                    if (tp > p || (tp == p && !tok.equals("^"))) {
                        out.add(ops.pop());
                    } else {
                        break;
                    }
                }
                ops.push(tok);
            } else {
                out.add(tok);
            }
        }
        while (!ops.isEmpty()) {
            out.add(ops.pop());
        }
        return out;
    }
}
