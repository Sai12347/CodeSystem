class LFUCache {
    private static class Node {
        int key;
        int val;
        int freq;
        Node prev;
        Node next;

        Node(int key, int val) {
            this.key = key;
            this.val = val;
            this.freq = 1;
        }
    }

    private static class DLL {
        final Node head = new Node(0, 0);
        final Node tail = new Node(0, 0);
        int size = 0;

        DLL() {
            head.next = tail;
            tail.prev = head;
        }

        void addFront(Node node) {
            node.prev = head;
            node.next = head.next;
            head.next.prev = node;
            head.next = node;
            size++;
        }

        void remove(Node node) {
            node.prev.next = node.next;
            node.next.prev = node.prev;
            size--;
        }

        Node popBack() {
            Node node = tail.prev;
            remove(node);
            return node;
        }
    }

    private final int capacity;
    private final Map<Integer, Node> keyMap;
    private final Map<Integer, DLL> freqMap;
    private int minFreq;

    public LFUCache(int capacity) {
        this.capacity = capacity;
        this.keyMap = new HashMap<>();
        this.freqMap = new HashMap<>();
        this.minFreq = 0;
    }

    private void touch(Node node) {
        int freq = node.freq;
        DLL bucket = freqMap.get(freq);
        bucket.remove(node);
        if (bucket.size == 0) {
            freqMap.remove(freq);
            if (minFreq == freq) {
                minFreq++;
            }
        }
        node.freq++;
        freqMap.computeIfAbsent(node.freq, k -> new DLL()).addFront(node);
    }

    public int get(int key) {
        Node node = keyMap.get(key);
        if (node == null) {
            return -1;
        }
        touch(node);
        return node.val;
    }

    public void put(int key, int value) {
        if (capacity <= 0) {
            return;
        }
        Node node = keyMap.get(key);
        if (node != null) {
            node.val = value;
            touch(node);
            return;
        }
        if (keyMap.size() == capacity) {
            DLL minBucket = freqMap.get(minFreq);
            Node evicted = minBucket.popBack();
            if (minBucket.size == 0) {
                freqMap.remove(minFreq);
            }
            keyMap.remove(evicted.key);
        }
        Node newNode = new Node(key, value);
        keyMap.put(key, newNode);
        minFreq = 1;
        freqMap.computeIfAbsent(1, k -> new DLL()).addFront(newNode);
    }
}
