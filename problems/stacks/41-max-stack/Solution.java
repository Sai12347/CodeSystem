class MaxStack {
    private final Deque<int[]> stack = new ArrayDeque<>();
    private final PriorityQueue<int[]> heap = new PriorityQueue<>(
        (a, b) -> a[0] != b[0] ? Integer.compare(b[0], a[0]) : Integer.compare(b[1], a[1])
    );
    private final Set<Integer> removed = new HashSet<>();
    private int nextId = 0;

    public MaxStack() {}

    private void cleanStack() {
        while (!stack.isEmpty() && removed.contains(stack.peek()[1])) {
            stack.pop();
        }
    }

    private void cleanHeap() {
        while (!heap.isEmpty() && removed.contains(heap.peek()[1])) {
            heap.poll();
        }
    }

    public void push(int x) {
        int id = nextId++;
        int[] item = new int[]{x, id};
        stack.push(item);
        heap.offer(item);
    }

    public int pop() {
        cleanStack();
        int[] item = stack.pop();
        removed.add(item[1]);
        return item[0];
    }

    public int top() {
        cleanStack();
        return stack.peek()[0];
    }

    public int peekMax() {
        cleanHeap();
        return heap.peek()[0];
    }

    public int popMax() {
        cleanHeap();
        int[] item = heap.poll();
        removed.add(item[1]);
        return item[0];
    }
}
