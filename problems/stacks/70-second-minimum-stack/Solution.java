class SecondMinStack {
    private final Deque<long[]> st = new ArrayDeque<>();

    public SecondMinStack() {}

    public void push(int val) {
        if (st.isEmpty()) {
            st.push(new long[]{val, val, Long.MAX_VALUE});
        } else {
            long[] prev = st.peek();
            long m1 = prev[1], m2 = prev[2];
            if (val < m1) {
                st.push(new long[]{val, val, m1});
            } else if (val < m2) {
                st.push(new long[]{val, m1, val});
            } else {
                st.push(new long[]{val, m1, m2});
            }
        }
    }

    public void pop() {
        st.pop();
    }

    public int top() {
        return (int) st.peek()[0];
    }

    public int getMin() {
        return (int) st.peek()[1];
    }

    public int getSecondMin() {
        return (int) st.peek()[2];
    }
}
