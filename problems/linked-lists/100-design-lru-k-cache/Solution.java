class LRUKCache {
    private static class Entry {
        int tier;
        int refTick;
        int ver;
        int key;

        Entry(int tier, int refTick, int ver, int key) {
            this.tier = tier;
            this.refTick = refTick;
            this.ver = ver;
            this.key = key;
        }
    }

    private final int cap;
    private final int k;
    private int tick = 0;
    private int seq = 0;
    private final Map<Integer, Integer> vals = new HashMap<>();
    private final Map<Integer, Deque<Integer>> hist = new HashMap<>();
    private final Map<Integer, Integer> ver = new HashMap<>();
    private final PriorityQueue<Entry> pq = new PriorityQueue<>((a, b) -> {
        if (a.tier != b.tier) return Integer.compare(a.tier, b.tier);
        if (a.refTick != b.refTick) return Integer.compare(a.refTick, b.refTick);
        return Integer.compare(a.ver, b.ver);
    });

    public LRUKCache(int capacity, int k) {
        this.cap = capacity;
        this.k = k;
    }

    private void recordAccess(int key) {
        tick++;
        Deque<Integer> dq = hist.get(key);
        dq.addLast(tick);
        if (dq.size() > k) {
            dq.removeFirst();
        }
        seq++;
        ver.put(key, seq);
        int tier = dq.size() < k ? 0 : 1;
        pq.offer(new Entry(tier, dq.peekFirst(), seq, key));
    }

    public int get(int key) {
        Integer val = vals.get(key);
        if (val == null) {
            return -1;
        }
        recordAccess(key);
        return val;
    }

    public void put(int key, int value) {
        if (vals.containsKey(key)) {
            vals.put(key, value);
            recordAccess(key);
            return;
        }
        if (vals.size() == cap) {
            while (!pq.isEmpty()) {
                Entry e = pq.poll();
                Integer curVer = ver.get(e.key);
                if (curVer != null && curVer == e.ver) {
                    vals.remove(e.key);
                    hist.remove(e.key);
                    ver.remove(e.key);
                    break;
                }
            }
        }
        vals.put(key, value);
        hist.put(key, new ArrayDeque<>());
        recordAccess(key);
    }
}
