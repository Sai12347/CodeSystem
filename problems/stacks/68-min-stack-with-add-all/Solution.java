class OffsetMinStack {
    private final Deque<long[]> st = new ArrayDeque<>();
    private long offset = 0L;

    public OffsetMinStack() {}

    public void push(int val) {
        long adj = (long) val - offset;
        long mn = st.isEmpty() ? adj : Math.min(adj, st.peek()[1]);
        st.push(new long[]{adj, mn});
    }

    public void pop() {
        st.pop();
    }

    public void addAll(int delta) {
        offset += delta;
    }

    public long top() {
        return st.peek()[0] + offset;
    }

    public long getMin() {
        return st.peek()[1] + offset;
    }
}
