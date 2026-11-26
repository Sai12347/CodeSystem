class Solution {
    public int longestBalancedPrefix(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(' || ch == '[' || ch == '{') {
                stack.push(ch);
            } else {
                if (stack.isEmpty()) break;
                char top = stack.peek();
                if ((ch == ')' && top == '(') || (ch == ']' && top == '[') || (ch == '}' && top == '{')) {
                    stack.pop();
                    if (stack.isEmpty()) best = i + 1;
                } else {
                    break;
                }
            }
        }
        return best;
    }
}
