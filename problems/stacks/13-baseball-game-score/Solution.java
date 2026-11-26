class Solution {
    public int calPoints(String[] operations) {
        Deque<Integer> stack = new ArrayDeque<>();
        for (String op : operations) {
            if (op.equals("C")) {
                stack.pop();
            } else if (op.equals("D")) {
                stack.push(stack.peek() * 2);
            } else if (op.equals("+")) {
                int top = stack.pop();
                int next = top + stack.peek();
                stack.push(top);
                stack.push(next);
            } else {
                stack.push(Integer.parseInt(op));
            }
        }
        int total = 0;
        for (int v : stack) total += v;
        return total;
    }
}
