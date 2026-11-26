class MinMaxSubarrayStack {
    private final List<long[]> st = new ArrayList<>();

    public MinMaxSubarrayStack() {
    }

    public void push(int val) {
        long v = val;
        if (st.isEmpty()) {
            st.add(new long[]{v, v, v, v, v});
        } else {
            long[] p = st.get(st.size() - 1);
            long cmin = Math.min(v, p[1] + v);
            long bmin = Math.min(p[2], cmin);
            long cmax = Math.max(v, p[3] + v);
            long bmax = Math.max(p[4], cmax);
            st.add(new long[]{v, cmin, bmin, cmax, bmax});
        }
    }

    public void pop() {
        st.remove(st.size() - 1);
    }

    public int top() {
        return (int) st.get(st.size() - 1)[0];
    }

    public long getMinSubarraySum() {
        return st.get(st.size() - 1)[2];
    }

    public long getMaxSubarraySum() {
        return st.get(st.size() - 1)[4];
    }
}
