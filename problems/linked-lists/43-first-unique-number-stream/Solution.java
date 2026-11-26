class FirstUnique {
    private static class Node {
        final int val;
        Node prev;
        Node next;

        Node(int val) {
            this.val = val;
        }
    }

    private final Node head;
    private final Node tail;
    private final Map<Integer, Node> nodes;

    public FirstUnique(int[] nums) {
        this.head = new Node(0);
        this.tail = new Node(0);
        this.head.next = this.tail;
        this.tail.prev = this.head;
        this.nodes = new HashMap<>();
        for (int x : nums) {
            add(x);
        }
    }

    private void append(Node node) {
        Node prev = tail.prev;
        prev.next = node;
        node.prev = prev;
        node.next = tail;
        tail.prev = node;
    }

    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    public int showFirstUnique() {
        if (head.next == tail) {
            return -1;
        }
        return head.next.val;
    }

    public void add(int value) {
        if (!nodes.containsKey(value)) {
            Node node = new Node(value);
            append(node);
            nodes.put(value, node);
        } else {
            Node existing = nodes.get(value);
            if (existing != null) {
                remove(existing);
                nodes.put(value, null);
            }
        }
    }
}
