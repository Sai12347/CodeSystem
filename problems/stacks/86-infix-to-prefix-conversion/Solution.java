class Solution {
    public String infixToPrefix(String s) {
        Deque<Character> ops = new ArrayDeque<>();
        StringBuilder out = new StringBuilder();
        for (int i = s.length() - 1; i >= 0; i--) {
            char ch = s.charAt(i);
            if (ch == ' ') continue;
            if (ch >= 'a' && ch <= 'z') {
                out.append(ch);
            } else if (ch == ')') {
                ops.push(ch);
            } else if (ch == '(') {
                while (!ops.isEmpty() && ops.peek() != ')') {
                    out.append(ops.pop());
                }
                ops.pop();
            } else {
                int p = (ch == '*' || ch == '/') ? 2 : 1;
                while (!ops.isEmpty() && ops.peek() != ')') {
                    char top = ops.peek();
                    int tp = (top == '*' || top == '/') ? 2 : 1;
                    if (tp > p) out.append(ops.pop());
                    else break;
                }
                ops.push(ch);
            }
        }
        while (!ops.isEmpty()) {
            out.append(ops.pop());
        }
        return out.reverse().toString();
    }
}
