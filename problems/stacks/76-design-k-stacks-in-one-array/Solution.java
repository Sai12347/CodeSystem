class KStacks {
    private final int[] data;
    private final int[] nxt;
    private final int[] top;
    private final int[] sizes;
    private int freeHead;

    public KStacks(int k, int capacity) {
        this.data = new int[capacity];
        this.nxt = new int[capacity];
        for (int i = 0; i < capacity - 1; i++) {
            this.nxt[i] = i + 1;
        }
        this.nxt[capacity - 1] = -1;
        this.top = new int[k];
        Arrays.fill(this.top, -1);
        this.sizes = new int[k];
        this.freeHead = 0;
    }

    public boolean push(int stackId, int val) {
        if (freeHead == -1) return false;
        int slot = freeHead;
        freeHead = nxt[slot];
        data[slot] = val;
        nxt[slot] = top[stackId];
        top[stackId] = slot;
        sizes[stackId]++;
        return true;
    }

    public int pop(int stackId) {
        int slot = top[stackId];
        if (slot == -1) return -1;
        top[stackId] = nxt[slot];
        nxt[slot] = freeHead;
        freeHead = slot;
        sizes[stackId]--;
        return data[slot];
    }

    public int peek(int stackId) {
        int slot = top[stackId];
        return slot == -1 ? -1 : data[slot];
    }

    public int size(int stackId) {
        return sizes[stackId];
    }
}
