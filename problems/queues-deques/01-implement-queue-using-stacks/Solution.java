class MyQueue {
    private final Deque<Integer> inStack = new ArrayDeque<>();
    private final Deque<Integer> outStack = new ArrayDeque<>();

    public MyQueue() {}

    private void shift() {
        if (outStack.isEmpty()) {
            while (!inStack.isEmpty()) {
                outStack.push(inStack.pop());
            }
        }
    }

    public void push(int x) {
        inStack.push(x);
    }

    public int pop() {
        shift();
        return outStack.pop();
    }

    public int peek() {
        shift();
        return outStack.peek();
    }

    public boolean empty() {
        return inStack.isEmpty() && outStack.isEmpty();
    }
}
