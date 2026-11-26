class TwoStacks {
    private final int[] arr;
    private final int cap;
    private int top1;
    private int top2;

    public TwoStacks(int capacity) {
        this.arr = new int[capacity];
        this.cap = capacity;
        this.top1 = -1;
        this.top2 = capacity;
    }

    public boolean push1(int val) {
        if (top1 + 1 == top2) return false;
        arr[++top1] = val;
        return true;
    }

    public boolean push2(int val) {
        if (top1 + 1 == top2) return false;
        arr[--top2] = val;
        return true;
    }

    public int pop1() {
        if (top1 == -1) return -1;
        return arr[top1--];
    }

    public int pop2() {
        if (top2 == cap) return -1;
        return arr[top2++];
    }

    public int size1() {
        return top1 + 1;
    }

    public int size2() {
        return cap - top2;
    }
}
