class Solution {
    public int minReversals(String s) {
        if (s.length() % 2 == 1) return -1;
        Deque<Character> stack = new ArrayDeque<>();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == ')' && !stack.isEmpty() && stack.peek() == '(') {
                stack.pop();
            } else {
                stack.push(ch);
            }
        }
        int opens = 0, closes = 0;
        for (char ch : stack) {
            if (ch == '(') opens++;
            else closes++;
        }
        return (opens + 1) / 2 + (closes + 1) / 2;
    }
}
