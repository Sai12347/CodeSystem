class MyCircularDeque {
    private final int[] buf;
    private final int cap;
    private int head;
    private int count;

    public MyCircularDeque(int k) {
        this.buf = new int[k];
        this.cap = k;
        this.head = 0;
        this.count = 0;
    }

    public boolean insertFront(int value) {
        if (count == cap) return false;
        head = (head - 1 + cap) % cap;
        buf[head] = value;
        count++;
        return true;
    }

    public boolean insertLast(int value) {
        if (count == cap) return false;
        buf[(head + count) % cap] = value;
        count++;
        return true;
    }

    public boolean deleteFront() {
        if (count == 0) return false;
        head = (head + 1) % cap;
        count--;
        return true;
    }

    public boolean deleteLast() {
        if (count == 0) return false;
        count--;
        return true;
    }

    public int getFront() {
        return count == 0 ? -1 : buf[head];
    }

    public int getRear() {
        return count == 0 ? -1 : buf[(head + count - 1) % cap];
    }

    public boolean isEmpty() {
        return count == 0;
    }

    public boolean isFull() {
        return count == cap;
    }
}
