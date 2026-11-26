class MiddleStack {
    private final Deque<Integer> left = new ArrayDeque<>();
    private final Deque<Integer> right = new ArrayDeque<>();

    public MiddleStack() {}

    private void rebalance() {
        while (left.size() > right.size() + 1) {
            right.addFirst(left.removeLast());
        }
        while (left.size() < right.size()) {
            left.addLast(right.removeFirst());
        }
    }

    public void push(int val) {
        right.addLast(val);
        rebalance();
    }

    public int pop() {
        int v;
        if (!right.isEmpty()) {
            v = right.removeLast();
        } else if (!left.isEmpty()) {
            v = left.removeLast();
        } else {
            return -1;
        }
        rebalance();
        return v;
    }

    public int top() {
        if (!right.isEmpty()) return right.peekLast();
        return left.isEmpty() ? -1 : left.peekLast();
    }

    public int getMiddle() {
        return left.isEmpty() ? -1 : left.peekLast();
    }

    public int popMiddle() {
        if (left.isEmpty()) return -1;
        int v = left.removeLast();
        rebalance();
        return v;
    }
}
