class Solution {
    public String parseTernary(String expression) {
        Deque<Character> stack = new ArrayDeque<>();
        for (int i = expression.length() - 1; i >= 0; i--) {
            char ch = expression.charAt(i);
            if (!stack.isEmpty() && stack.peek() == '?') {
                stack.pop();
                char tVal = stack.pop();
                char fVal = stack.pop();
                stack.push(ch == 'T' ? tVal : fVal);
            } else if (ch != ':') {
                stack.push(ch);
            }
        }
        return String.valueOf(stack.peek());
    }
}
