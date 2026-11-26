class RecentCounter {
    private final Deque<Integer> q = new ArrayDeque<>();

    public RecentCounter() {}

    public int ping(int t) {
        q.offerLast(t);
        int cutoff = t - 3000;
        while (q.peekFirst() < cutoff) {
            q.pollFirst();
        }
        return q.size();
    }
}
