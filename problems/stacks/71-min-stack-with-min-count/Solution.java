class CountMinStack {
    private final Deque<int[]> st = new ArrayDeque<>();

    public CountMinStack() {}

    public void push(int val) {
        if (st.isEmpty()) {
            st.push(new int[]{val, val, 1});
        } else {
            int[] prev = st.peek();
            if (val < prev[1]) {
                st.push(new int[]{val, val, 1});
            } else if (val == prev[1]) {
                st.push(new int[]{val, prev[1], prev[2] + 1});
            } else {
                st.push(new int[]{val, prev[1], prev[2]});
            }
        }
    }

    public void pop() {
        st.pop();
    }

    public int top() {
        return st.peek()[0];
    }

    public int getMin() {
        return st.peek()[1];
    }

    public int getMinCount() {
        return st.peek()[2];
    }
}
