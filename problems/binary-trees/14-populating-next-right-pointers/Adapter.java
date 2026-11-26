class Node {
    public int val;
    public Node left;
    public Node right;
    public Node next;

    public Node() {}

    public Node(int _val) {
        val = _val;
    }

    public Node(int _val, Node _left, Node _right, Node _next) {
        val = _val;
        left = _left;
        right = _right;
        next = _next;
    }
}

class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> vals = (List<Object>) inp.get("root");
        int n = vals.size();
        Node[] nodes = new Node[n];
        int[] origVals = new int[n];
        for (int i = 0; i < n; i++) {
            origVals[i] = ((Number) vals.get(i)).intValue();
            nodes[i] = new Node(origVals[i]);
        }
        for (int i = 0; i < n; i++) {
            int li = 2 * i + 1;
            int ri = 2 * i + 2;
            if (li < n) nodes[i].left = nodes[li];
            if (ri < n) nodes[i].right = nodes[ri];
        }

        Node origRoot = n > 0 ? nodes[0] : null;
        Node ans = new Solution().connect(origRoot);

        if (n == 0) {
            if (ans != null) return "ERROR: expected null for empty tree";
            return new ArrayList<>();
        }
        if (ans != origRoot) {
            return "ERROR: must return the original root node";
        }

        IdentityHashMap<Node, Boolean> valid = new IdentityHashMap<>();
        for (int i = 0; i < n; i++) {
            Node expLeft = (2 * i + 1 < n) ? nodes[2 * i + 1] : null;
            Node expRight = (2 * i + 2 < n) ? nodes[2 * i + 2] : null;
            if (nodes[i].val != origVals[i] || nodes[i].left != expLeft || nodes[i].right != expRight) {
                return "ERROR: tree node values or left/right pointers were modified";
            }
            valid.put(nodes[i], Boolean.TRUE);
        }

        List<Object> out = new ArrayList<>();
        Node level = ans;
        while (level != null) {
            Node cur = level;
            IdentityHashMap<Node, Boolean> seen = new IdentityHashMap<>();
            while (cur != null) {
                if (!valid.containsKey(cur)) {
                    return "ERROR: next pointer points outside the original tree";
                }
                if (seen.put(cur, Boolean.TRUE) != null) {
                    return "ERROR: cycle detected in next pointers";
                }
                out.add((long) cur.val);
                cur = cur.next;
            }
            out.add("#");
            level = level.left;
        }
        return out;
    }
}
