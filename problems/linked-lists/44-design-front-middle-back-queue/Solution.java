class FrontMiddleBackQueue {
    private final Deque<Integer> left;
    private final Deque<Integer> right;

    public FrontMiddleBackQueue() {
        this.left = new ArrayDeque<>();
        this.right = new ArrayDeque<>();
    }

    private void rebalance() {
        if (left.size() > right.size() + 1) {
            right.addFirst(left.removeLast());
        } else if (left.size() < right.size()) {
            left.addLast(right.removeFirst());
        }
    }

    public void pushFront(int val) {
        left.addFirst(val);
        rebalance();
    }

    public void pushMiddle(int val) {
        if (left.size() > right.size()) {
            right.addFirst(left.removeLast());
        }
        left.addLast(val);
    }

    public void pushBack(int val) {
        right.addLast(val);
        rebalance();
    }

    public int popFront() {
        if (left.isEmpty()) {
            return -1;
        }
        int val = left.removeFirst();
        rebalance();
        return val;
    }

    public int popMiddle() {
        if (left.isEmpty()) {
            return -1;
        }
        int val = left.removeLast();
        rebalance();
        return val;
    }

    public int popBack() {
        if (left.isEmpty()) {
            return -1;
        }
        if (right.isEmpty()) {
            return left.removeLast();
        }
        int val = right.removeLast();
        rebalance();
        return val;
    }
}
