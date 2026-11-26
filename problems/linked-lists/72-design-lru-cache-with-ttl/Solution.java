class TTLLRUCache {
    private static class Node {
        int key, val, exp, ver;
        Node prev, next;
        Node(int key, int val, int exp, int ver) {
            this.key = key;
            this.val = val;
            this.exp = exp;
            this.ver = ver;
        }
    }

    private final int cap;
    private final Map<Integer, Node> map = new HashMap<>();
    private final PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> {
        if (a[0] != b[0]) return Integer.compare(a[0], b[0]);
        return Integer.compare(a[1], b[1]);
    });
    private int ver = 0;
    private final Node head = new Node(0, 0, 0, 0);
    private final Node tail = new Node(0, 0, 0, 0);

    public TTLLRUCache(int capacity) {
        this.cap = capacity;
        head.next = tail;
        tail.prev = head;
    }

    private void unlink(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void insertFront(Node node) {
        node.prev = head;
        node.next = head.next;
        head.next.prev = node;
        head.next = node;
    }

    private void purge(int timestamp) {
        while (!heap.isEmpty() && heap.peek()[0] <= timestamp) {
            int[] top = heap.poll();
            Node node = map.get(top[2]);
            if (node != null && node.ver == top[1]) {
                unlink(node);
                map.remove(top[2]);
            }
        }
    }

    public int get(int key, int timestamp) {
        purge(timestamp);
        Node node = map.get(key);
        if (node == null) {
            return -1;
        }
        unlink(node);
        insertFront(node);
        return node.val;
    }

    public void put(int key, int value, int timestamp, int ttl) {
        purge(timestamp);
        ver++;
        int exp = timestamp + ttl;
        Node node = map.get(key);
        if (node != null) {
            node.val = value;
            node.exp = exp;
            node.ver = ver;
            unlink(node);
            insertFront(node);
        } else {
            if (map.size() == cap) {
                Node lru = tail.prev;
                unlink(lru);
                map.remove(lru.key);
            }
            node = new Node(key, value, exp, ver);
            insertFront(node);
            map.put(key, node);
        }
        heap.offer(new int[]{exp, ver, key});
    }
}
