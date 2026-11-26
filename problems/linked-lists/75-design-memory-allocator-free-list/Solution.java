class MemoryAllocator {
    private static class Node {
        int start, length, mid;
        Node prev, next;
        Node(int start, int length, int mid) {
            this.start = start;
            this.length = length;
            this.mid = mid;
        }
    }

    private final Node head = new Node(0, 0, -1);
    private final Node tail = new Node(0, 0, -1);
    private final Map<Integer, List<Node>> owned = new HashMap<>();

    public MemoryAllocator(int n) {
        Node first = new Node(0, n, 0);
        head.next = first;
        first.prev = head;
        first.next = tail;
        tail.prev = first;
    }

    private void unlink(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void insertBefore(Node ref, Node node) {
        node.prev = ref.prev;
        node.next = ref;
        ref.prev.next = node;
        ref.prev = node;
    }

    public int allocate(int size, int mID) {
        Node curr = head.next;
        while (curr != tail) {
            if (curr.mid == 0 && curr.length >= size) {
                int addr = curr.start;
                Node alloc;
                if (curr.length == size) {
                    curr.mid = mID;
                    alloc = curr;
                } else {
                    alloc = new Node(addr, size, mID);
                    curr.start += size;
                    curr.length -= size;
                    insertBefore(curr, alloc);
                }
                owned.computeIfAbsent(mID, k -> new ArrayList<>()).add(alloc);
                return addr;
            }
            curr = curr.next;
        }
        return -1;
    }

    public int freeMemory(int mID) {
        List<Node> nodes = owned.remove(mID);
        if (nodes == null || nodes.isEmpty()) {
            return 0;
        }
        int freed = 0;
        for (Node node : nodes) {
            freed += node.length;
            node.mid = 0;
            if (node.prev != head && node.prev.mid == 0) {
                Node left = node.prev;
                node.start = left.start;
                node.length += left.length;
                unlink(left);
            }
            if (node.next != tail && node.next.mid == 0) {
                Node right = node.next;
                node.length += right.length;
                unlink(right);
            }
        }
        return freed;
    }
}
