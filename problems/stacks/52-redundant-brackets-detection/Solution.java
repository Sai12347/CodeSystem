class Solution {
    public boolean hasRedundantBrackets(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == ')') {
                boolean hasOp = false;
                while (!stack.isEmpty() && stack.peek() != '(') {
                    char top = stack.pop();
                    if (top == '+' || top == '-' || top == '*' || top == '/') {
                        hasOp = true;
                    }
                }
                if (!stack.isEmpty()) stack.pop();
                if (!hasOp) return true;
            } else {
                stack.push(ch);
            }
        }
        return false;
    }
}
