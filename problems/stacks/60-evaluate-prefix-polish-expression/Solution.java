class Solution {
    public int evalPrefix(String[] tokens) {
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = tokens.length - 1; i >= 0; i--) {
            String tok = tokens[i];
            if (tok.equals("+") || tok.equals("-") || tok.equals("*") || tok.equals("/")) {
                int a = stack.pop();
                int b = stack.pop();
                if (tok.equals("+")) stack.push(a + b);
                else if (tok.equals("-")) stack.push(a - b);
                else if (tok.equals("*")) stack.push(a * b);
                else stack.push(a / b);
            } else {
                stack.push(Integer.parseInt(tok));
            }
        }
        return stack.peek();
    }
}
