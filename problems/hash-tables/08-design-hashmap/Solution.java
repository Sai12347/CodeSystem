class MyHashMap {
    private static class Node {
        int key;
        int val;
        Node next;

        Node(int key, int val, Node next) {
            this.key = key;
            this.val = val;
            this.next = next;
        }
    }

    private static final int SIZE = 2069;
    private final Node[] buckets = new Node[SIZE];

    public MyHashMap() {
    }

    public void put(int key, int value) {
        int idx = key % SIZE;
        Node curr = buckets[idx];
        while (curr != null) {
            if (curr.key == key) {
                curr.val = value;
                return;
            }
            curr = curr.next;
        }
        buckets[idx] = new Node(key, value, buckets[idx]);
    }

    public int get(int key) {
        int idx = key % SIZE;
        Node curr = buckets[idx];
        while (curr != null) {
            if (curr.key == key) {
                return curr.val;
            }
            curr = curr.next;
        }
        return -1;
    }

    public void remove(int key) {
        int idx = key % SIZE;
        Node curr = buckets[idx];
        Node prev = null;
        while (curr != null) {
            if (curr.key == key) {
                if (prev == null) {
                    buckets[idx] = curr.next;
                } else {
                    prev.next = curr.next;
                }
                return;
            }
            prev = curr;
            curr = curr.next;
        }
    }
}
