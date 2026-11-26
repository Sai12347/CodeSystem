class SLRUCache {
    private static class Node {
        int key, val, seg;
        Node prev, next;

        Node(int k, int v, int s) {
            this.key = k;
            this.val = v;
            this.seg = s;
        }
    }

    private static class DLL {
        final Node head = new Node(0, 0, 0);
        final Node tail = new Node(0, 0, 0);
        int size = 0;

        DLL() {
            head.next = tail;
            tail.prev = head;
        }

        void addFront(Node node) {
            Node nxt = head.next;
            head.next = node;
            node.prev = head;
            node.next = nxt;
            nxt.prev = node;
            size++;
        }

        void unlink(Node node) {
            node.prev.next = node.next;
            node.next.prev = node.prev;
            size--;
        }

        Node popBack() {
            Node node = tail.prev;
            unlink(node);
            return node;
        }
    }

    private final int probCap;
    private final int protCap;
    private final DLL prob = new DLL();
    private final DLL prot = new DLL();
    private final Map<Integer, Node> map = new HashMap<>();

    public SLRUCache(int probationCap, int protectedCap) {
        this.probCap = probationCap;
        this.protCap = protectedCap;
    }

    private void promote(Node node) {
        prob.unlink(node);
        if (prot.size == protCap) {
            Node demoted = prot.popBack();
            demoted.seg = 1;
            prob.addFront(demoted);
        }
        node.seg = 2;
        prot.addFront(node);
    }

    public int get(int key) {
        Node node = map.get(key);
        if (node == null) {
            return -1;
        }
        if (node.seg == 2) {
            prot.unlink(node);
            prot.addFront(node);
        } else {
            promote(node);
        }
        return node.val;
    }

    public void put(int key, int value) {
        Node node = map.get(key);
        if (node != null) {
            node.val = value;
            if (node.seg == 2) {
                prot.unlink(node);
                prot.addFront(node);
            } else {
                promote(node);
            }
            return;
        }
        if (prob.size == probCap) {
            Node victim = prob.popBack();
            map.remove(victim.key);
        }
        node = new Node(key, value, 1);
        map.put(key, node);
        prob.addFront(node);
    }

    public int segmentOf(int key) {
        Node node = map.get(key);
        return node == null ? 0 : node.seg;
    }
}
