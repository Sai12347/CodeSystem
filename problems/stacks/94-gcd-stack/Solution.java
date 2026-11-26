class GcdStack {
    private final Deque<Integer> vals = new ArrayDeque<>();
    private final Deque<Integer> gcds = new ArrayDeque<>();

    public GcdStack() {
    }

    private int gcd(int a, int b) {
        while (b != 0) {
            int t = a % b;
            a = b;
            b = t;
        }
        return a;
    }

    public void push(int val) {
        vals.push(val);
        if (gcds.isEmpty()) gcds.push(val);
        else gcds.push(gcd(gcds.peek(), val));
    }

    public void pop() {
        vals.pop();
        gcds.pop();
    }

    public int top() {
        return vals.peek();
    }

    public int getGcd() {
        return gcds.peek();
    }
}
