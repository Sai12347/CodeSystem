class HitCounter {
    private final Deque<int[]> q = new ArrayDeque<>();
    private int total = 0;

    public HitCounter() {}

    private void evict(int timestamp) {
        int cutoff = timestamp - 300;
        while (!q.isEmpty() && q.peekFirst()[0] <= cutoff) {
            total -= q.pollFirst()[1];
        }
    }

    public void hit(int timestamp) {
        evict(timestamp);
        if (!q.isEmpty() && q.peekLast()[0] == timestamp) {
            q.peekLast()[1]++;
        } else {
            q.offerLast(new int[]{timestamp, 1});
        }
        total++;
    }

    public int getHits(int timestamp) {
        evict(timestamp);
        return total;
    }
}
