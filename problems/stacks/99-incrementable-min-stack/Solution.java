class IncrementableMinStack {
    private final int cap;
    private int sz;
    private final long[] mn;
    private final long[] lazy;

    public IncrementableMinStack(int maxSize) {
        this.cap = maxSize;
        this.sz = 0;
        this.mn = new long[4 * maxSize + 4];
        this.lazy = new long[4 * maxSize + 4];
    }

    private void pushDown(int node) {
        long lz = lazy[node];
        if (lz != 0L) {
            int lc = node << 1;
            int rc = lc | 1;
            mn[lc] += lz;
            lazy[lc] += lz;
            mn[rc] += lz;
            lazy[rc] += lz;
            lazy[node] = 0L;
        }
    }

    private void pointSet(int node, int l, int r, int pos, long val) {
        if (l == r) {
            mn[node] = val;
            lazy[node] = 0L;
            return;
        }
        pushDown(node);
        int mid = (l + r) >>> 1;
        if (pos <= mid) pointSet(node << 1, l, mid, pos, val);
        else pointSet((node << 1) | 1, mid + 1, r, pos, val);
        mn[node] = Math.min(mn[node << 1], mn[(node << 1) | 1]);
    }

    private void rangeAdd(int node, int l, int r, int ql, int qr, long delta) {
        if (ql <= l && r <= qr) {
            mn[node] += delta;
            lazy[node] += delta;
            return;
        }
        pushDown(node);
        int mid = (l + r) >>> 1;
        if (ql <= mid) rangeAdd(node << 1, l, mid, ql, qr, delta);
        if (qr > mid) rangeAdd((node << 1) | 1, mid + 1, r, ql, qr, delta);
        mn[node] = Math.min(mn[node << 1], mn[(node << 1) | 1]);
    }

    private long rangeMin(int node, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return mn[node];
        pushDown(node);
        int mid = (l + r) >>> 1;
        if (qr <= mid) return rangeMin(node << 1, l, mid, ql, qr);
        if (ql > mid) return rangeMin((node << 1) | 1, mid + 1, r, ql, qr);
        return Math.min(rangeMin(node << 1, l, mid, ql, qr), rangeMin((node << 1) | 1, mid + 1, r, ql, qr));
    }

    public void push(int val) {
        if (sz == cap) return;
        pointSet(1, 0, cap - 1, sz, val);
        sz++;
    }

    public long pop() {
        long res = rangeMin(1, 0, cap - 1, sz - 1, sz - 1);
        sz--;
        return res;
    }

    public void increment(int k, int delta) {
        if (sz == 0 || k <= 0 || delta == 0) return;
        int r = Math.min(k, sz) - 1;
        rangeAdd(1, 0, cap - 1, 0, r, delta);
    }

    public long top() {
        return rangeMin(1, 0, cap - 1, sz - 1, sz - 1);
    }

    public long getMin() {
        return rangeMin(1, 0, cap - 1, 0, sz - 1);
    }
}
