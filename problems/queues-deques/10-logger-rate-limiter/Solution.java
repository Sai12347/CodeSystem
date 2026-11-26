class Logger {
    private record Entry(int ts, String msg) {}

    private final Deque<Entry> q = new ArrayDeque<>();
    private final Set<String> active = new HashSet<>();

    public Logger() {}

    public boolean shouldPrintMessage(int timestamp, String message) {
        int cutoff = timestamp - 10;
        while (!q.isEmpty() && q.peekFirst().ts() <= cutoff) {
            active.remove(q.pollFirst().msg());
        }
        if (active.contains(message)) {
            return false;
        }
        active.add(message);
        q.offerLast(new Entry(timestamp, message));
        return true;
    }
}
