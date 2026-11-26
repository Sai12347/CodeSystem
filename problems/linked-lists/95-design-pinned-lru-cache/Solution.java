class PinnedLRUCache {
    private static class Node {
        int key, val;
        boolean pinned;
        Node prev, next;

        Node(int k, int v) {
            this.key = k;
            this.val = v;
        }
    }

    private final int cap;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(0, 0);
    private final Node tail = new Node(0, 0);

    public PinnedLRUCache(int capacity) {
        this.cap = capacity;
        head.next = tail;
        tail.prev = head;
    }

    private void unlink(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
        node.prev = null;
        node.next = null;
    }

    private void addFront(Node node) {
        Node nxt = head.next;
        head.next = node;
        node.prev = head;
        node.next = nxt;
        nxt.prev = node;
    }

    public int get(int key) {
        Node node = map.get(key);
        if (node == null) {
            return -1;
        }
        if (!node.pinned) {
            unlink(node);
            addFront(node);
        }
        return node.val;
    }

    public boolean put(int key, int value) {
        Node node = map.get(key);
        if (node != null) {
            node.val = value;
            if (!node.pinned) {
                unlink(node);
                addFront(node);
            }
            return true;
        }
        if (map.size() == cap) {
            if (tail.prev == head) {
                return false;
            }
            Node victim = tail.prev;
            unlink(victim);
            map.remove(victim.key);
        }
        node = new Node(key, value);
        map.put(key, node);
        addFront(node);
        return true;
    }

    public boolean pin(int key) {
        Node node = map.get(key);
        if (node == null) {
            return false;
        }
        if (!node.pinned) {
            unlink(node);
            node.pinned = true;
        }
        return true;
    }

    public boolean unpin(int key) {
        Node node = map.get(key);
        if (node == null) {
            return false;
        }
        if (node.pinned) {
            node.pinned = false;
            addFront(node);
        }
        return true;
    }
}
