class Solution {
    public int longestMultiBracketSubstring(String s) {
        Deque<int[]> stack = new ArrayDeque<>();
        stack.push(new int[]{'#', -1});
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(' || ch == '[' || ch == '{') {
                stack.push(new int[]{ch, i});
            } else {
                char need = ch == ')' ? '(' : (ch == ']' ? '[' : '{');
                if (stack.peek()[0] == need) {
                    stack.pop();
                    int span = i - stack.peek()[1];
                    if (span > best) best = span;
                } else {
                    stack.push(new int[]{ch, i});
                }
            }
        }
        return best;
    }
}
