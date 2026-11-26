class AllOneTracker {
    private static class Bucket {
        final int count;
        final Set<String> keys = new HashSet<>();
        Bucket prev;
        Bucket next;

        Bucket(int count) {
            this.count = count;
        }
    }

    private final Bucket head;
    private final Bucket tail;
    private final Map<String, Bucket> keyMap;

    public AllOneTracker() {
        head = new Bucket(0);
        tail = new Bucket(0);
        head.next = tail;
        tail.prev = head;
        keyMap = new HashMap<>();
    }

    private Bucket insertAfter(Bucket prev, int count) {
        Bucket node = new Bucket(count);
        Bucket nxt = prev.next;
        prev.next = node;
        node.prev = prev;
        node.next = nxt;
        nxt.prev = node;
        return node;
    }

    private void removeIfEmpty(Bucket node) {
        if (node.keys.isEmpty()) {
            node.prev.next = node.next;
            node.next.prev = node.prev;
        }
    }

    public void inc(String key) {
        Bucket cur = keyMap.get(key);
        if (cur == null) {
            Bucket target = (head.next == tail || head.next.count != 1)
                ? insertAfter(head, 1)
                : head.next;
            target.keys.add(key);
            keyMap.put(key, target);
            return;
        }
        int nxtCnt = cur.count + 1;
        Bucket target = (cur.next == tail || cur.next.count != nxtCnt)
            ? insertAfter(cur, nxtCnt)
            : cur.next;
        target.keys.add(key);
        keyMap.put(key, target);
        cur.keys.remove(key);
        removeIfEmpty(cur);
    }

    public void dec(String key) {
        Bucket cur = keyMap.get(key);
        if (cur == null) {
            return;
        }
        if (cur.count == 1) {
            keyMap.remove(key);
        } else {
            int prvCnt = cur.count - 1;
            Bucket target = (cur.prev == head || cur.prev.count != prvCnt)
                ? insertAfter(cur.prev, prvCnt)
                : cur.prev;
            target.keys.add(key);
            keyMap.put(key, target);
        }
        cur.keys.remove(key);
        removeIfEmpty(cur);
    }

    public int getMaxCount() {
        return head.next == tail ? 0 : tail.prev.count;
    }

    public int getMinCount() {
        return head.next == tail ? 0 : head.next.count;
    }

    public int getCount(String key) {
        Bucket b = keyMap.get(key);
        return b == null ? 0 : b.count;
    }
}
