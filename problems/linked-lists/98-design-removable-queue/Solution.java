class RemovableQueue {
    private static class Node {
        int val;
        Node prev, next;

        Node(int v) {
            this.val = v;
        }
    }

    private final Node head = new Node(0);
    private final Node tail = new Node(0);
    private final Map<Integer, Node> map = new HashMap<>();

    public RemovableQueue() {
        head.next = tail;
        tail.prev = head;
    }

    private void unlink(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    public boolean enqueue(int id) {
        if (map.containsKey(id)) {
            return false;
        }
        Node node = new Node(id);
        Node prev = tail.prev;
        prev.next = node;
        node.prev = prev;
        node.next = tail;
        tail.prev = node;
        map.put(id, node);
        return true;
    }

    public int dequeue() {
        if (map.isEmpty()) {
            return -1;
        }
        Node node = head.next;
        unlink(node);
        map.remove(node.val);
        return node.val;
    }

    public boolean cancel(int id) {
        Node node = map.remove(id);
        if (node == null) {
            return false;
        }
        unlink(node);
        return true;
    }

    public int peekFront() {
        if (map.isEmpty()) {
            return -1;
        }
        return head.next.val;
    }

    public int size() {
        return map.size();
    }
}
