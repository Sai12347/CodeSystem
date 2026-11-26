class Solution {
    public int expressionTreeHeight(String s) {
        Deque<Integer> heights = new ArrayDeque<>();
        Deque<Character> ops = new ArrayDeque<>();
        int i = 0, n = s.length();
        while (i < n) {
            char ch = s.charAt(i);
            if (ch == ' ') {
                i++;
            } else if (ch >= '0' && ch <= '9') {
                while (i < n && s.charAt(i) >= '0' && s.charAt(i) <= '9') i++;
                heights.push(0);
            } else if (ch == '(') {
                ops.push(ch);
                i++;
            } else if (ch == ')') {
                while (!ops.isEmpty() && ops.peek() != '(') {
                    applyOp(heights, ops);
                }
                ops.pop();
                i++;
            } else {
                int p = (ch == '*' || ch == '/') ? 2 : 1;
                while (!ops.isEmpty() && ops.peek() != '(' && ((ops.peek() == '*' || ops.peek() == '/') ? 2 : 1) >= p) {
                    applyOp(heights, ops);
                }
                ops.push(ch);
                i++;
            }
        }
        while (!ops.isEmpty()) {
            applyOp(heights, ops);
        }
        return heights.peek();
    }

    private void applyOp(Deque<Integer> heights, Deque<Character> ops) {
        ops.pop();
        int hr = heights.pop();
        int hl = heights.pop();
        heights.push(1 + Math.max(hl, hr));
    }
}
