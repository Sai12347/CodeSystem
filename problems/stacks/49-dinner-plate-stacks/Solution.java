class DinnerPlates {
    private final int cap;
    private final List<Deque<Integer>> stacks = new ArrayList<>();
    private final PriorityQueue<Integer> avail = new PriorityQueue<>();

    public DinnerPlates(int capacity) {
        this.cap = capacity;
    }

    public void push(int val) {
        while (!avail.isEmpty() && (avail.peek() >= stacks.size() || stacks.get(avail.peek()).size() == cap)) {
            avail.poll();
        }
        if (!avail.isEmpty()) {
            int idx = avail.peek();
            stacks.get(idx).push(val);
            if (stacks.get(idx).size() == cap) {
                avail.poll();
            }
        } else {
            Deque<Integer> st = new ArrayDeque<>();
            st.push(val);
            stacks.add(st);
            if (cap > 1) {
                avail.offer(stacks.size() - 1);
            }
        }
    }

    public int pop() {
        while (!stacks.isEmpty() && stacks.get(stacks.size() - 1).isEmpty()) {
            stacks.remove(stacks.size() - 1);
        }
        if (stacks.isEmpty()) return -1;
        int idx = stacks.size() - 1;
        int val = stacks.get(idx).pop();
        while (!stacks.isEmpty() && stacks.get(stacks.size() - 1).isEmpty()) {
            stacks.remove(stacks.size() - 1);
        }
        if (idx < stacks.size()) {
            avail.offer(idx);
        }
        return val;
    }

    public int popAtStack(int index) {
        if (index < 0 || index >= stacks.size() || stacks.get(index).isEmpty()) {
            return -1;
        }
        int val = stacks.get(index).pop();
        while (!stacks.isEmpty() && stacks.get(stacks.size() - 1).isEmpty()) {
            stacks.remove(stacks.size() - 1);
        }
        if (index < stacks.size()) {
            avail.offer(index);
        }
        return val;
    }
}
