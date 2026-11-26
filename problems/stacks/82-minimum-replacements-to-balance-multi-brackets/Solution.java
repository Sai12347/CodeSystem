class Solution {
    public int minBracketReplacements(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        int reps = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(' || ch == '[' || ch == '{' || ch == '<') {
                stack.push(ch);
            } else {
                if (stack.isEmpty()) return -1;
                char top = stack.pop();
                char need = ch == ')' ? '(' : (ch == ']' ? '[' : (ch == '}' ? '{' : '<'));
                if (top != need) reps++;
            }
        }
        return stack.isEmpty() ? reps : -1;
    }
}
