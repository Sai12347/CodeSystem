class AffineMinStack {
    private final Deque<Long> vals = new ArrayDeque<>();
    private final Deque<Long> mins = new ArrayDeque<>();
    private final Deque<Long> maxs = new ArrayDeque<>();
    private long sign = 1L;
    private long offset = 0L;

    public AffineMinStack() {
    }

    public void push(int val) {
        long stored = sign * ((long) val - offset);
        vals.push(stored);
        if (mins.isEmpty()) {
            mins.push(stored);
            maxs.push(stored);
        } else {
            mins.push(Math.min(stored, mins.peek()));
            maxs.push(Math.max(stored, maxs.peek()));
        }
    }

    public void pop() {
        vals.pop();
        mins.pop();
        maxs.pop();
    }

    public void addAll(int delta) {
        offset += delta;
    }

    public void negateAll() {
        sign = -sign;
        offset = -offset;
    }

    public long top() {
        return sign * vals.peek() + offset;
    }

    public long getMin() {
        if (sign == 1L) return mins.peek() + offset;
        return -maxs.peek() + offset;
    }
}
