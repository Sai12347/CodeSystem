class CustomStack {
    private final int[] stack;
    private final int[] inc;
    private int top;

    public CustomStack(int maxSize) {
        this.stack = new int[maxSize];
        this.inc = new int[maxSize];
        this.top = 0;
    }

    public void push(int x) {
        if (top < stack.length) {
            stack[top] = x;
            inc[top] = 0;
            top++;
        }
    }

    public int pop() {
        if (top == 0) return -1;
        int idx = --top;
        int add = inc[idx];
        if (idx > 0) inc[idx - 1] += add;
        return stack[idx] + add;
    }

    public void increment(int k, int val) {
        int idx = Math.min(k, top) - 1;
        if (idx >= 0) inc[idx] += val;
    }
}
