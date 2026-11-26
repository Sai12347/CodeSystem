class Node {
    public int val;
    public Node prev;
    public Node next;
    public Node child;

    public Node() {}

    public Node(int val) {
        this.val = val;
    }

    public Node(int val, Node prev, Node next, Node child) {
        this.val = val;
        this.prev = prev;
        this.next = next;
        this.child = child;
    }
}

class Adapter {
    @SuppressWarnings("unchecked")
    private static Node buildLevel(List<Object> items, int[] counter) {
        Node head = null;
        Node tail = null;
        for (Object item : items) {
            if (item instanceof List) {
                if (tail == null) {
                    throw new IllegalArgumentException("Child list without preceding node");
                }
                tail.child = buildLevel((List<Object>) item, counter);
            } else {
                Node node = new Node(((Number) item).intValue());
                counter[0]++;
                if (head == null) {
                    head = node;
                    tail = node;
                } else {
                    tail.next = node;
                    node.prev = tail;
                    tail = node;
                }
            }
        }
        return head;
    }

    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> spec = (List<Object>) inp.get("head");
        int[] counter = {0};
        Node root = (spec == null || spec.isEmpty()) ? null : buildLevel(spec, counter);
        int total = counter[0];

        Node ans = new Solution().flatten(root);

        if (total == 0) {
            if (ans != null) {
                return "ERROR: expected null for empty input";
            }
            return new ArrayList<>();
        }
        if (ans == null) {
            return new ArrayList<>();
        }
        if (ans.prev != null) {
            return "ERROR: head.prev must be null";
        }

        List<Object> out = new ArrayList<>(total);
        IdentityHashMap<Node, Boolean> seen = new IdentityHashMap<>();
        Node cur = ans;
        while (cur != null) {
            if (seen.containsKey(cur)) {
                return "ERROR: returned list contains a cycle";
            }
            seen.put(cur, Boolean.TRUE);
            if (cur.child != null) {
                return "ERROR: node " + cur.val + " still has a non-null child pointer";
            }
            if (cur.next != null && cur.next.prev != cur) {
                return "ERROR: broken prev pointer after node " + cur.val;
            }
            out.add((long) cur.val);
            if (out.size() > total) {
                return "ERROR: returned list has more nodes than input";
            }
            cur = cur.next;
        }

        if (out.size() != total) {
            return "ERROR: expected " + total + " nodes, got " + out.size();
        }
        return out;
    }
}
