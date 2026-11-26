class Solution {
    public String reverseParentheses(String s) {
        int n = s.length();
        int[] pair = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (ch == '(') {
                stack.push(i);
            } else if (ch == ')') {
                int j = stack.pop();
                pair[i] = j;
                pair[j] = i;
            }
        }
        StringBuilder out = new StringBuilder();
        int i = 0, d = 1;
        while (i < n) {
            char ch = s.charAt(i);
            if (ch == '(' || ch == ')') {
                i = pair[i];
                d = -d;
            } else {
                out.append(ch);
            }
            i += d;
        }
        return out.toString();
    }
}
