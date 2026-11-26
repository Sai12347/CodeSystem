class MinStack {
    private final Deque<Integer> stack = new ArrayDeque<>();
    private final Deque<Integer> mins = new ArrayDeque<>();

    public MinStack() {}

    public void push(int val) {
        stack.push(val);
        if (mins.isEmpty() || val <= mins.peek()) {
            mins.push(val);
        }
    }

    public void pop() {
        if (stack.pop().equals(mins.peek())) {
            mins.pop();
        }
    }

    public int top() {
        return stack.peek();
    }

    public int getMin() {
        return mins.peek();
    }
}
