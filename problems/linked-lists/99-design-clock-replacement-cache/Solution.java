class ClockCache {
    private static class Node {
        int key, val, ref;
        Node prev, next;

        Node(int k, int v) {
            this.key = k;
            this.val = v;
            this.ref = 1;
            this.prev = this;
            this.next = this;
        }
    }

    private final int cap;
    private Node hand = null;
    private final Map<Integer, Node> map = new HashMap<>();

    public ClockCache(int capacity) {
        this.cap = capacity;
    }

    public int get(int key) {
        Node node = map.get(key);
        if (node == null) {
            return -1;
        }
        node.ref = 1;
        return node.val;
    }

    public void put(int key, int value) {
        Node node = map.get(key);
        if (node != null) {
            node.val = value;
            node.ref = 1;
            return;
        }
        if (map.size() < cap) {
            node = new Node(key, value);
            if (hand == null) {
                hand = node;
            } else {
                Node prev = hand.prev;
                prev.next = node;
                node.prev = prev;
                node.next = hand;
                hand.prev = node;
            }
            map.put(key, node);
            return;
        }
        while (hand.ref == 1) {
            hand.ref = 0;
            hand = hand.next;
        }
        map.remove(hand.key);
        hand.key = key;
        hand.val = value;
        hand.ref = 1;
        map.put(key, hand);
        hand = hand.next;
    }
}
