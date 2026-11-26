class Solution {
    public int evalRPN(String[] tokens) {
        Deque<Integer> stack = new ArrayDeque<>();
        for (String tok : tokens) {
            switch (tok) {
                case "+" -> stack.push(stack.pop() + stack.pop());
                case "-" -> {
                    int b = stack.pop();
                    int a = stack.pop();
                    stack.push(a - b);
                }
                case "*" -> stack.push(stack.pop() * stack.pop());
                case "/" -> {
                    int b = stack.pop();
                    int a = stack.pop();
                    stack.push(a / b);
                }
                default -> stack.push(Integer.parseInt(tok));
            }
        }
        return stack.pop();
    }
}
