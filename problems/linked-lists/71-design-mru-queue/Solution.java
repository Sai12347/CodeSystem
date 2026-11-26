class MRUQueue {
    private final int block;
    private final LinkedList<Integer>[] buckets;

    @SuppressWarnings("unchecked")
    public MRUQueue(int n) {
        this.block = Math.max(1, (int) Math.sqrt(n));
        int numBuckets = (n + block - 1) / block;
        this.buckets = new LinkedList[numBuckets];
        for (int i = 0; i < numBuckets; i++) {
            buckets[i] = new LinkedList<>();
            int start = i * block + 1;
            int end = Math.min(n, start + block - 1);
            for (int v = start; v <= end; v++) {
                buckets[i].addLast(v);
            }
        }
    }

    public int fetch(int k) {
        int b = (k - 1) / block;
        int off = (k - 1) % block;
        int val = buckets[b].remove(off);
        for (int j = b; j < buckets.length - 1; j++) {
            buckets[j].addLast(buckets[j + 1].removeFirst());
        }
        buckets[buckets.length - 1].addLast(val);
        return val;
    }
}
