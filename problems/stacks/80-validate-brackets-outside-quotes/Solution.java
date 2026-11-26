class Solution {
    public boolean isValidOutsideQuotes(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        boolean inQuote = false;
        boolean escaped = false;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (inQuote) {
                if (escaped) {
                    escaped = false;
                } else if (ch == '\\') {
                    escaped = true;
                } else if (ch == '"') {
                    inQuote = false;
                }
            } else {
                if (ch == '"') {
                    inQuote = true;
                } else if (ch == '(' || ch == '[' || ch == '{') {
                    stack.push(ch);
                } else if (ch == ')' || ch == ']' || ch == '}') {
                    char need = ch == ')' ? '(' : (ch == ']' ? '[' : '{');
                    if (stack.isEmpty() || stack.peek() != need) return false;
                    stack.pop();
                }
            }
        }
        return !inQuote && stack.isEmpty();
    }
}
