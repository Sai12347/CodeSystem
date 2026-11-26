class WeightedLRUCache {
    private static class Node {
        int key, val, weight;
        Node prev, next;

        Node(int k, int v, int w) {
            this.key = k;
            this.val = v;
            this.weight = w;
        }
    }

    private final int maxWeight;
    private int totalWeight = 0;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(0, 0, 0);
    private final Node tail = new Node(0, 0, 0);

    public WeightedLRUCache(int maxWeight) {
        this.maxWeight = maxWeight;
        head.next = tail;
        tail.prev = head;
    }

    private void unlink(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
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
        unlink(node);
        addFront(node);
        return node.val;
    }

    public boolean put(int key, int value, int weight) {
        if (weight > maxWeight) {
            return false;
        }
        Node old = map.get(key);
        if (old != null) {
            unlink(old);
            totalWeight -= old.weight;
            map.remove(key);
        }
        while (totalWeight + weight > maxWeight) {
            Node victim = tail.prev;
            unlink(victim);
            totalWeight -= victim.weight;
            map.remove(victim.key);
        }
        Node node = new Node(key, value, weight);
        map.put(key, node);
        addFront(node);
        totalWeight += weight;
        return true;
    }

    public int currentWeight() {
        return totalWeight;
    }
}
