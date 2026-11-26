class BoundedMinStack {
    private final int[] vals;
    private final int[] mins;
    private final int[] minIdx;
    private int sz;

    public BoundedMinStack(int capacity) {
        this.vals = new int[capacity];
        this.mins = new int[capacity];
        this.minIdx = new int[capacity];
        this.sz = 0;
    }

    public boolean push(int val) {
        if (sz == vals.length) return false;
        vals[sz] = val;
        if (sz == 0 || val < mins[sz - 1]) {
            mins[sz] = val;
            minIdx[sz] = sz;
        } else {
            mins[sz] = mins[sz - 1];
            minIdx[sz] = minIdx[sz - 1];
        }
        sz++;
        return true;
    }

    public int pop() {
        if (sz == 0) return -1;
        return vals[--sz];
    }

    public int top() {
        return sz == 0 ? -1 : vals[sz - 1];
    }

    public int getMin() {
        return sz == 0 ? -1 : mins[sz - 1];
    }

    public int getMinIndex() {
        return sz == 0 ? -1 : minIdx[sz - 1];
    }
}
