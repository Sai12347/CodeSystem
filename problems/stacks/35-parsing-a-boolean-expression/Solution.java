class Solution {
    public boolean parseBoolExpr(String expression) {
        Deque<Character> stack = new ArrayDeque<>();
        for (int i = 0; i < expression.length(); i++) {
            char ch = expression.charAt(i);
            if (ch == ',') continue;
            if (ch != ')') {
                stack.push(ch);
            } else {
                boolean hasT = false, hasF = false;
                while (stack.peek() != '(') {
                    char v = stack.pop();
                    if (v == 't') hasT = true;
                    else hasF = true;
                }
                stack.pop();
                char op = stack.pop();
                char res;
                if (op == '!') res = hasF ? 't' : 'f';
                else if (op == '&') res = hasF ? 'f' : 't';
                else res = hasT ? 't' : 'f';
                stack.push(res);
            }
        }
        return stack.peek() == 't';
    }
}
