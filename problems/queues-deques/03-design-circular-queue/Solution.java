class MyCircularQueue {
    private final int[] buf;
    private final int cap;
    private int head;
    private int count;

    public MyCircularQueue(int k) {
        this.buf = new int[k];
        this.cap = k;
        this.head = 0;
        this.count = 0;
    }

    public boolean enQueue(int value) {
        if (count == cap) return false;
        buf[(head + count) % cap] = value;
        count++;
        return true;
    }

    public boolean deQueue() {
        if (count == 0) return false;
        head = (head + 1) % cap;
        count--;
        return true;
    }

    public int Front() {
        return count == 0 ? -1 : buf[head];
    }

    public int Rear() {
        return count == 0 ? -1 : buf[(head + count - 1) % cap];
    }

    public boolean isEmpty() {
        return count == 0;
    }

    public boolean isFull() {
        return count == cap;
    }
}
