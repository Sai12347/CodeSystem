class Solution {
    public String removeParentheses(String s) {
        Deque<Integer> signStack = new ArrayDeque<>();
        signStack.push(1);
        int localSign = 1;
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '+') {
                localSign = 1;
            } else if (ch == '-') {
                localSign = -1;
            } else if (ch == '(') {
                signStack.push(signStack.peek() * localSign);
                localSign = 1;
            } else if (ch == ')') {
                signStack.pop();
            } else {
                int eff = signStack.peek() * localSign;
                if (eff == -1) {
                    out.append('-');
                } else if (out.length() > 0) {
                    out.append('+');
                }
                out.append(ch);
                localSign = 1;
            }
        }
        return out.toString();
    }
}
