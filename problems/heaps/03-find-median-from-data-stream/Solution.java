class MedianFinder {
    private final PriorityQueue<Integer> lo; // max-heap for smaller half
    private final PriorityQueue<Integer> hi; // min-heap for larger half

    public MedianFinder() {
        lo = new PriorityQueue<>(Collections.reverseOrder());
        hi = new PriorityQueue<>();
    }

    public void addNum(int num) {
        lo.offer(num);
        hi.offer(lo.poll());
        if (hi.size() > lo.size()) {
            lo.offer(hi.poll());
        }
    }

    public double findMedian() {
        if (lo.size() > hi.size()) {
            return (double) lo.peek();
        }
        return (lo.peek() + hi.peek()) / 2.0;
    }
}
