class RangeStack {
    private final Deque<int[]> st = new ArrayDeque<>();

    public RangeStack() {}

    public void push(int val) {
        if (st.isEmpty()) {
            st.push(new int[]{val, val, val});
        } else {
            int[] prev = st.peek();
            st.push(new int[]{val, Math.min(val, prev[1]), Math.max(val, prev[2])});
        }
    }

    public void pop() {
        st.pop();
    }

    public int top() {
        return st.peek()[0];
    }

    public long getRange() {
        int[] cur = st.peek();
        return (long) cur[2] - (long) cur[1];
    }
}
