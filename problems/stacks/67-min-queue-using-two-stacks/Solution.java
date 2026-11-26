class MinQueue {
    private final Deque<int[]> inSt = new ArrayDeque<>();
    private final Deque<int[]> outSt = new ArrayDeque<>();

    public MinQueue() {}

    private void pour() {
        if (outSt.isEmpty()) {
            while (!inSt.isEmpty()) {
                int val = inSt.pop()[0];
                int mn = outSt.isEmpty() ? val : Math.min(val, outSt.peek()[1]);
                outSt.push(new int[]{val, mn});
            }
        }
    }

    public void enqueue(int val) {
        int mn = inSt.isEmpty() ? val : Math.min(val, inSt.peek()[1]);
        inSt.push(new int[]{val, mn});
    }

    public int dequeue() {
        pour();
        return outSt.pop()[0];
    }

    public int front() {
        pour();
        return outSt.peek()[0];
    }

    public int getMin() {
        if (inSt.isEmpty()) return outSt.peek()[1];
        if (outSt.isEmpty()) return inSt.peek()[1];
        return Math.min(inSt.peek()[1], outSt.peek()[1]);
    }
}
